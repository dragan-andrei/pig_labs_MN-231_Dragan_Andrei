"""Primary GUI View implementation built on CustomTkinter."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

import customtkinter

from presenter.presenter_interface import IComputerPresenter
from view.theme import PurpleTheme
from view.view_interface import IComputerView
from view.view_model import DeviceViewModel
from view.widgets.header_banner import HeaderBannerView
from view.widgets.sort_button_bar import SortButtonBar
from view.widgets.device_card import DeviceCard
from view.widgets.device_form import DeviceFormDialog
from view.services.image_repository import DeviceImageRepository


class ComputerView(IComputerView):
    """Main CustomTkinter window implementing the IComputerView abstraction."""

    def __init__(self) -> None:
        """Initialize GUI window, containers, and layout."""
        self._presenter: Optional[IComputerPresenter] = None
        self._window = customtkinter.CTk()
        self._device_cards: list[DeviceCard] = []
        self._image_repository = DeviceImageRepository(
            Path(__file__).resolve().parents[1] / "assets" / "devices"
        )
        self._setup_window()
        self._create_layout()

    def set_presenter(self, presenter: IComputerPresenter) -> None:
        """Register presenter to receive user interaction callbacks.

        Args:
            presenter: The presenter instance mediating between model and view.
        """
        self._presenter = presenter

    def _setup_window(self) -> None:
        """Configure main window properties and purple theme background."""
        self._window.title("Lab 2 GUI - Computer Catalog")
        self._window.geometry("820x760")
        self._window.minsize(680, 700)
        self._window.configure(fg_color=PurpleTheme.BG_WINDOW)

    def _create_layout(self) -> None:
        """Construct the layout matching Lab 2 geometry and widgets."""
        self._window.grid_columnconfigure(0, weight=1)
        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_rowconfigure(1, weight=0)

        # Main content container (Row 0)
        main_container = customtkinter.CTkFrame(
            self._window,
            fg_color="transparent",
        )
        main_container.grid(row=0, column=0, padx=18, pady=(18, 12), sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(0, weight=0)
        main_container.grid_rowconfigure(1, weight=0)
        main_container.grid_rowconfigure(2, weight=1)

        # 1. Header Banner
        self._header_banner = HeaderBannerView(main_container)
        self._header_banner.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        # 2. Scrollable list of individual device cards
        self._device_scroll = customtkinter.CTkScrollableFrame(
            main_container,
            fg_color=PurpleTheme.BG_CARD_CONTAINER,
            corner_radius=8,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
        )
        self._device_scroll.grid(row=1, column=0, rowspan=2, sticky="nsew", pady=(0, 8))
        self._device_scroll.grid_columnconfigure(0, weight=1)

        # 3. Bottom toolbar with add and sort actions
        self._button_bar = SortButtonBar(
            self._window,
            on_sort_requested=self._handle_sort_clicked,
        )
        self._button_bar.grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")
        self._add_button = customtkinter.CTkButton(
            self._window,
            text="＋ Добавить устройство",
            command=self._open_add_dialog,
            fg_color=PurpleTheme.BTN_ACTIVE_BG,
            hover_color=PurpleTheme.BTN_ACTIVE_HOVER,
        )
        self._add_button.grid(row=2, column=0, padx=18, pady=(0, 18), sticky="ew")

    def _handle_sort_clicked(self, key_name: str) -> None:
        """Callback triggered by toolbar buttons, delegating directly to presenter.

        Args:
            key_name: Attribute key ('cpu', 'ram', 'storage') requested for ordering.
        """
        if self._presenter is not None:
            self._presenter.handle_sort_requested(key_name)

    def _open_add_dialog(self) -> None:
        """Open the add-device form."""
        if self._presenter is not None:
            DeviceFormDialog(self._window, ("PC", "Laptop", "Server"), self._presenter.handle_add_requested)

    def _open_edit_dialog(self, device: DeviceViewModel) -> None:
        """Open the edit form for one card."""
        if self._presenter is not None:
            DeviceFormDialog(
                self._window,
                ("PC", "Laptop", "Server"),
                lambda device_type, values: self._presenter.handle_edit_requested(device.device_index, device_type, values),
                device,
            )

    def _delete_device(self, index: int) -> None:
        """Forward a card delete action to the presenter."""
        if self._presenter is not None:
            self._presenter.handle_delete_requested(index)

    def display_devices(
        self,
        devices: Sequence[DeviceViewModel],
        status_description: str,
        total_count: int,
    ) -> None:
        """Render formatted device rows into the textbox and update header counters.

        Args:
            devices: Sequence of DeviceViewModel items prepared by the presenter.
            status_description: Human-readable text indicating current sort state.
            total_count: Count of devices displayed.
        """
        self._header_banner.update_status(total_count, status_description)

        for card in self._device_cards:
            card.destroy()
        self._device_cards.clear()
        for row_number, device in enumerate(devices, start=1):
            card = DeviceCard(
                self._device_scroll,
                device,
                on_edit=self._open_edit_dialog,
                on_delete=self._delete_device,
                image_provider=self._image_repository,
                row_number=row_number,
            )
            card.grid(row=row_number - 1, column=0, padx=10, pady=(8 if row_number == 1 else 4, 4), sticky="ew")
            self._device_cards.append(card)

    def update_sort_button_state(
        self,
        active_key: Optional[str],
        direction_arrow: Optional[str],
    ) -> None:
        """Forward sort button visual state update to toolbar widget.

        Args:
            active_key: Active strategy key name, or None.
            direction_arrow: Active arrow indicator, or None.
        """
        self._button_bar.update_active_state(active_key, direction_arrow)

    def show_error(self, message: str) -> None:
        """Update header banner with error alert.

        Args:
            message: Descriptive error message.
        """
        self._header_banner.update_status(0, f"ERROR: {message}")

    def start(self) -> None:
        """Start the CustomTkinter main event loop."""
        self._window.mainloop()

    def close(self) -> None:
        """Destroy the application window."""
        self._window.destroy()

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(presenter={self._presenter!r})"

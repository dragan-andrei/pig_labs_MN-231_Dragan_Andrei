"""Primary GUI View implementation built on CustomTkinter."""

from __future__ import annotations

from typing import Optional, Sequence

import customtkinter

from presenter.presenter_interface import IComputerPresenter
from view.theme import PurpleTheme
from view.view_interface import IComputerView
from view.view_model import DeviceViewModel
from view.widgets.header_banner import HeaderBannerView
from view.widgets.sort_button_bar import SortButtonBar
from view.widgets.table_header import TableHeaderView


class ComputerView(IComputerView):
    """Main CustomTkinter window implementing the IComputerView abstraction."""

    def __init__(self) -> None:
        """Initialize GUI window, containers, and layout."""
        self._presenter: Optional[IComputerPresenter] = None
        self._window = customtkinter.CTk()
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

        # 2. Table Column Headers
        self._table_header = TableHeaderView(main_container)
        self._table_header.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        # 3. Monospace Device Display Textbox
        self._device_textbox = customtkinter.CTkTextbox(
            main_container,
            height=590,
            fg_color=PurpleTheme.BG_CARD_CONTAINER,
            corner_radius=8,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
            font=("Cascadia Mono", 12),
            activate_scrollbars=False,
        )
        self._device_textbox.grid(row=2, column=0, sticky="nsew")
        self._device_textbox.bind("<MouseWheel>", lambda event: "break")
        self._device_textbox.bind("<Button-4>", lambda event: "break")
        self._device_textbox.bind("<Button-5>", lambda event: "break")

        # Color syntax tags for monospace row formatting
        self._device_textbox.tag_config("title", foreground=PurpleTheme.TEXT_ACCENT)
        self._device_textbox.tag_config("header", foreground=PurpleTheme.TEXT_PRIMARY)
        self._device_textbox.tag_config("separator", foreground=PurpleTheme.BORDER_HEADER)
        self._device_textbox.tag_config("pc", foreground=PurpleTheme.BADGE_PC_TEXT)
        self._device_textbox.tag_config("laptop", foreground=PurpleTheme.BADGE_LAPTOP_TEXT)
        self._device_textbox.tag_config("server", foreground=PurpleTheme.BADGE_SERVER_TEXT)
        self._device_textbox.tag_config("device", foreground=PurpleTheme.TEXT_PRIMARY)
        self._device_textbox.configure(state="disabled")

        # 4. Bottom Toolbar with sort action buttons (Row 1)
        self._button_bar = SortButtonBar(
            self._window,
            on_sort_requested=self._handle_sort_clicked,
        )
        self._button_bar.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="ew")

    def _handle_sort_clicked(self, key_name: str) -> None:
        """Callback triggered by toolbar buttons, delegating directly to presenter.

        Args:
            key_name: Attribute key ('cpu', 'ram', 'storage') requested for ordering.
        """
        if self._presenter is not None:
            self._presenter.handle_sort_requested(key_name)

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

        type_width = 12
        cpu_width = 29
        ram_width = 10
        storage_width = 12
        details_width = 18
        line_length = type_width + cpu_width + ram_width + storage_width + details_width

        self._device_textbox.configure(state="normal")
        self._device_textbox.delete("1.0", "end")
        self._device_textbox.insert("end", f"{status_description}\n", "title")
        self._device_textbox.insert("end", "\n")
        self._device_textbox.insert("end", "-" * line_length + "\n", "separator")

        for dev in devices:
            tag = dev.type_name.lower()
            self._device_textbox.insert("end", f"{dev.type_name:<{type_width}}", tag)
            self._device_textbox.insert(
                "end",
                f"{dev.cpu_text:<{cpu_width}}"
                f"{dev.ram_text:>{ram_width}}"
                f"{dev.storage_text:>{storage_width}}"
                f"{dev.extra_text:>{details_width}}\n",
            )

        self._device_textbox.configure(state="disabled")

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

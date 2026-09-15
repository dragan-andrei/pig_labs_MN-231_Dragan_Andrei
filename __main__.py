"""Modern Object-Oriented CustomTkinter GUI for Computer Catalog."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Final, List, Optional, Sequence, Tuple

import customtkinter

from computers.laptop import Laptop
from computers.pc import PC
from computers.server import Server
from interface.interface import Interface


# ==============================================================================
# Domain Exceptions
# ==============================================================================

class DomainError(Exception):
    """Base domain exception for the laboratory application."""


class SortStrategyError(DomainError):
    """Raised when sorting strategy fails or encounters invalid keys."""


# ==============================================================================
# Color Palette & Theme Constants
# ==============================================================================

class PurpleTheme:
    """Design tokens and color palette maintaining a refined purple aesthetic."""

    # Backgrounds
    BG_WINDOW: Final[str] = "#140f1c"
    BG_CARD_CONTAINER: Final[str] = "#191224"
    BG_CARD_EVEN: Final[str] = "#1e152a"
    BG_CARD_ODD: Final[str] = "#241833"
    BG_HEADER_ROW: Final[str] = "#291a3c"
    BG_BUTTON_BAR: Final[str] = "#251333"

    # Borders & Dividers
    BORDER_SUBTLE: Final[str] = "#36204d"
    BORDER_HEADER: Final[str] = "#4c2c6d"
    BORDER_ACTIVE: Final[str] = "#8b5cf6"

    # Button States
    BTN_DEFAULT_BG: Final[str] = "#51386d"
    BTN_DEFAULT_HOVER: Final[str] = "#68488a"
    BTN_ACTIVE_BG: Final[str] = "#7b47a6"
    BTN_ACTIVE_HOVER: Final[str] = "#9156c2"

    # Typography & Foreground
    TEXT_PRIMARY: Final[str] = "#f5eefc"
    TEXT_SECONDARY: Final[str] = "#bca9d3"
    TEXT_MUTED: Final[str] = "#8d79a5"
    TEXT_ACCENT: Final[str] = "#d8b4fe"

    # Type Badges
    BADGE_PC_BG: Final[str] = "#2e1b4a"
    BADGE_PC_TEXT: Final[str] = "#c084fc"
    BADGE_LAPTOP_BG: Final[str] = "#3d1b40"
    BADGE_LAPTOP_TEXT: Final[str] = "#f472b6"
    BADGE_SERVER_BG: Final[str] = "#201f4c"
    BADGE_SERVER_TEXT: Final[str] = "#93c5fd"


# ==============================================================================
# Sorting Strategy Pattern
# ==============================================================================

class SortDirection(Enum):
    """Enumeration representing sorting order."""

    DESCENDING = "descending"
    ASCENDING = "ascending"

    @property
    def arrow(self) -> str:
        """Return directional arrow indicator for UI representation."""
        return "▼" if self == SortDirection.DESCENDING else "▲"

    @property
    def label(self) -> str:
        """Return human-readable text label."""
        return "от большего к меньшему" if self == SortDirection.DESCENDING else "от меньшего к большему"

    def toggle(self) -> SortDirection:
        """Toggle between ascending and descending order."""
        return SortDirection.ASCENDING if self == SortDirection.DESCENDING else SortDirection.DESCENDING


class ISortStrategy(ABC):
    """Contract for sorting collections of computer devices."""

    @property
    @abstractmethod
    def key_name(self) -> str:
        """Return internal parameter key used for extraction."""

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Return human-readable strategy title."""

    @abstractmethod
    def sort(self, items: List[Interface], direction: SortDirection) -> List[Interface]:
        """Sort the given list of devices according to strategy rules.

        Args:
            items: The list of devices to sort.
            direction: SortDirection specifying ascending or descending order.

        Returns:
            The sorted list of devices.

        Raises:
            SortStrategyError: If an error occurs during comparison.
        """


class CpuPowerCatalog:
    """Reference benchmark points used to compare CPU performance.

    The values are normalized CPU Mark-style scores for the exact models in
    the catalog. A higher score means a more powerful processor.
    """

    _SCORES: dict[str, int] = {
        "Intel Core i3": 9000,
        "Intel Core i5": 15000,
        "Intel Core i7": 22000,
        "Intel Core i9": 30000,
        "AMD Ryzen 3": 9500,
        "AMD Ryzen 5": 18000,
        "AMD Ryzen 7": 24000,
        "AMD Ryzen 9": 34000,
        "Intel Core i5-13400": 25000,
        "AMD Ryzen 5 5600X": 22000,
        "Apple M1": 14500,
        "Apple M2": 16000,
        "Apple M3": 20500,
        "Intel Core i5-1240P": 17500,
        "Intel Core i7-12700H": 27500,
        "AMD Ryzen 7 6800U": 21500,
        "Intel Core Ultra 7": 29000,
        "AMD Ryzen 9 7940HS": 31500,
        "Apple M2 Pro": 24500,
        "Apple M3 Max": 48000,
        "AMD EPYC 7763": 64000,
        "AMD EPYC 9654": 96000,
        "Intel Xeon Silver 4314": 22000,
        "Intel Xeon Gold 6330": 40000,
        "Intel Xeon Platinum 8380": 54000,
        "AMD EPYC 7543": 56000,
        "Intel Xeon E-2388G": 18000,
        "AMD EPYC 9354": 60000,
        "Intel Xeon Gold 5418Y": 36000,
        "AMD EPYC 7713": 52000,
    }

    @classmethod
    def score_for(cls, cpu_name: object) -> int:
        """Return the benchmark score for a CPU model."""
        return cls._SCORES.get(str(cpu_name), 0)


class CpuSortStrategy(ISortStrategy):
    """Sort strategy based on processor performance scores."""

    @property
    def key_name(self) -> str:
        return "cpu"

    @property
    def display_name(self) -> str:
        return "CPU Power"

    def sort(self, items: List[Interface], direction: SortDirection) -> List[Interface]:
        try:
            return sorted(
                items,
                key=lambda item: CpuPowerCatalog.score_for(item.get_parameter(self.key_name)),
                reverse=(direction == SortDirection.DESCENDING),
            )
        except Exception as err:
            raise SortStrategyError(f"Failed to sort by CPU: {err}") from err


class RamSortStrategy(ISortStrategy):
    """Sort strategy for RAM capacity in gigabytes."""

    @property
    def key_name(self) -> str:
        return "ram"

    @property
    def display_name(self) -> str:
        return "RAM"

    def sort(self, items: List[Interface], direction: SortDirection) -> List[Interface]:
        try:
            return sorted(
                items,
                key=lambda item: int(item.get_parameter(self.key_name) or 0),
                reverse=(direction == SortDirection.DESCENDING),
            )
        except Exception as err:
            raise SortStrategyError(f"Failed to sort by RAM: {err}") from err


class StorageSortStrategy(ISortStrategy):
    """Sort strategy for Storage capacity in gigabytes."""

    @property
    def key_name(self) -> str:
        return "storage"

    @property
    def display_name(self) -> str:
        return "Storage"

    def sort(self, items: List[Interface], direction: SortDirection) -> List[Interface]:
        try:
            return sorted(
                items,
                key=lambda item: int(item.get_parameter(self.key_name) or 0),
                reverse=(direction == SortDirection.DESCENDING),
            )
        except Exception as err:
            raise SortStrategyError(f"Failed to sort by Storage: {err}") from err


# ==============================================================================
# Presenter / Adapter Pattern for Polymorphic UI Rendering
# ==============================================================================

class IDevicePresenter(ABC):
    """Abstraction defining how a computer entity is represented on the UI."""

    @property
    @abstractmethod
    def type_badge(self) -> Tuple[str, str, str]:
        """Return (label, background_color, text_color)."""

    @property
    @abstractmethod
    def cpu_text(self) -> str:
        """Return formatted CPU string."""

    @property
    @abstractmethod
    def ram_text(self) -> str:
        """Return formatted RAM string."""

    @property
    @abstractmethod
    def storage_text(self) -> str:
        """Return formatted Storage string."""

    @property
    @abstractmethod
    def extra_text(self) -> str:
        """Return device-specific formatted detail string."""


class BaseDevicePresenter(IDevicePresenter):
    """Base presenter for standard Computer devices."""

    def __init__(self, device: Interface) -> None:
        self._device = device

    @property
    def type_badge(self) -> Tuple[str, str, str]:
        return "DEVICE", PurpleTheme.BADGE_PC_BG, PurpleTheme.BADGE_PC_TEXT

    @property
    def cpu_text(self) -> str:
        return str(self._device.get_parameter("cpu") or "N/A")

    @property
    def ram_text(self) -> str:
        ram = self._device.get_parameter("ram")
        return f"{ram} GB" if ram is not None else "N/A"

    @property
    def storage_text(self) -> str:
        storage = self._device.get_parameter("storage")
        if storage is None:
            return "N/A"
        return f"{storage} GB"

    @property
    def extra_text(self) -> str:
        return "-"


class PCDevicePresenter(BaseDevicePresenter):
    """Presenter specialized for Desktop PCs."""

    @property
    def type_badge(self) -> Tuple[str, str, str]:
        return "PC", PurpleTheme.BADGE_PC_BG, PurpleTheme.BADGE_PC_TEXT

    @property
    def extra_text(self) -> str:
        form = self._device.get_parameter("form_factor")
        return str(form) if form else "-"


class LaptopDevicePresenter(BaseDevicePresenter):
    """Presenter specialized for Laptops."""

    @property
    def type_badge(self) -> Tuple[str, str, str]:
        return "Laptop", PurpleTheme.BADGE_LAPTOP_BG, PurpleTheme.BADGE_LAPTOP_TEXT

    @property
    def extra_text(self) -> str:
        battery = self._device.get_parameter("battery_life")
        return f"{battery} hrs" if battery is not None else "-"


class ServerDevicePresenter(BaseDevicePresenter):
    """Presenter specialized for Rack Servers."""

    @property
    def type_badge(self) -> Tuple[str, str, str]:
        return "Server", PurpleTheme.BADGE_SERVER_BG, PurpleTheme.BADGE_SERVER_TEXT

    @property
    def extra_text(self) -> str:
        rack = self._device.get_parameter("rack_units")
        return f"{rack}U Rack" if rack is not None else "-"


class DevicePresenterFactory:
    """Factory creating appropriate presenter adapters for devices."""

    @staticmethod
    def create(device: Interface) -> IDevicePresenter:
        """Create a dedicated presenter instance based on device type.

        Args:
            device: An entity implementing Interface.

        Returns:
            An IDevicePresenter instance.
        """
        device_type = device.__class__.__name__.lower()
        if "laptop" in device_type:
            return LaptopDevicePresenter(device)
        if "server" in device_type:
            return ServerDevicePresenter(device)
        if "pc" in device_type:
            return PCDevicePresenter(device)
        return BaseDevicePresenter(device)


# ==============================================================================
# GUI Components
# ==============================================================================

class StatusTicker(customtkinter.CTkLabel):
    """Animated status line that cycles through short system messages."""

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        super().__init__(
            parent,
            text="// DATA STREAM :: READY",
            font=("Cascadia Mono", 10),
            text_color=PurpleTheme.TEXT_MUTED,
            anchor="w",
        )
        self._messages = (
            "// DATA STREAM :: READY",
            "// SORT ENGINE :: ARMED",
            "// CATALOG LINK :: STABLE",
            "// SYSTEM PULSE :: NOMINAL",
        )
        self._message_index = 0
        self._animation_id: str | None = None
        self._animate()

    def _animate(self) -> None:
        """Cycle the status text on a lightweight timer."""
        message = self._messages[self._message_index]
        self._message_index = (self._message_index + 1) % len(self._messages)
        self.configure(text=message)
        self._animation_id = self.after(1100, self._animate)

    def destroy(self) -> None:
        """Cancel the ticker timer before destroying the label."""
        if self._animation_id is not None:
            self.after_cancel(self._animation_id)
            self._animation_id = None
        super().destroy()


class ActivityIndicator(customtkinter.CTkFrame):
    """Small animated activity indicator for the application header."""

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        super().__init__(parent, fg_color="transparent")
        self._frames = ("◐", "◓", "◑", "◒")
        self._frame_index = 0
        self._is_online = True
        self._animation_id: str | None = None
        self._toggle_button = customtkinter.CTkButton(
            self,
            text="◐ LIVE",
            command=self._toggle_status,
            font=("Consolas", 11, "bold"),
            text_color=PurpleTheme.TEXT_ACCENT,
            fg_color="transparent",
            hover_color=PurpleTheme.BG_BUTTON_BAR,
            width=82,
            height=28,
        )
        self._toggle_button.pack(padx=4, pady=4)
        self._pulse_bar = customtkinter.CTkProgressBar(
            self,
            mode="indeterminate",
            width=82,
            height=4,
            progress_color=PurpleTheme.BORDER_ACTIVE,
        )
        self._pulse_bar.pack(padx=4, pady=(0, 4))
        self._pulse_bar.start()
        self._animate()

    def _animate(self) -> None:
        """Advance the indicator without blocking the Tkinter event loop."""
        if not self._is_online:
            return
        frame = self._frames[self._frame_index]
        self._frame_index = (self._frame_index + 1) % len(self._frames)
        self._toggle_button.configure(text=f"{frame} LIVE")
        self._animation_id = self.after(180, self._animate)

    def _toggle_status(self) -> None:
        """Toggle the activity animation between LIVE and OFFLINE."""
        self._is_online = not self._is_online
        if self._is_online:
            self._toggle_button.configure(
                text="◐ LIVE",
                text_color=PurpleTheme.TEXT_ACCENT,
            )
            self._pulse_bar.start()
            self._animate()
            return

        if self._animation_id is not None:
            self.after_cancel(self._animation_id)
            self._animation_id = None
        self._pulse_bar.stop()
        self._toggle_button.configure(
            text="○ OFFLINE",
            text_color=PurpleTheme.TEXT_MUTED,
        )

    def destroy(self) -> None:
        """Cancel the scheduled animation before destroying the widget."""
        if self._animation_id is not None:
            self.after_cancel(self._animation_id)
            self._animation_id = None
        self._pulse_bar.stop()
        super().destroy()


class HeaderBannerView(customtkinter.CTkFrame):
    """Application header banner showing catalog title and status counters."""

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        super().__init__(
            parent,
            fg_color=PurpleTheme.BG_HEADER_ROW,
            corner_radius=8,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
        )
        self._title_label = customtkinter.CTkLabel(
            self,
            text="⚡ Computer Systems Catalog",
            font=("Segoe UI", 16, "bold"),
            text_color=PurpleTheme.TEXT_PRIMARY,
        )
        self._status_badge = customtkinter.CTkLabel(
            self,
            text="30 devices | Исходный порядок",
            font=("Segoe UI", 12),
            text_color=PurpleTheme.TEXT_ACCENT,
            fg_color=PurpleTheme.BG_BUTTON_BAR,
            corner_radius=6,
            padx=12,
            pady=4,
        )
        self._activity_indicator = ActivityIndicator(self)
        self._status_ticker = StatusTicker(self)
        self._layout_widgets()

    def _layout_widgets(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self._title_label.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        self._status_badge.grid(row=0, column=1, padx=16, pady=10, sticky="e")
        self._activity_indicator.grid(row=0, column=2, padx=(0, 10), pady=0, sticky="e")
        self._status_ticker.grid(row=1, column=0, columnspan=3, padx=16, pady=(0, 8), sticky="ew")

    def update_status(self, total_count: int, order_description: str) -> None:
        """Update the header status label text.

        Args:
            total_count: Current number of devices displayed.
            order_description: Descriptive title of the current sort state.
        """
        self._status_badge.configure(text=f"{total_count} устройств • {order_description}")


class TableHeaderView(customtkinter.CTkFrame):
    """Fixed column header bar for the device grid table."""

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        super().__init__(
            parent,
            fg_color=PurpleTheme.BG_HEADER_ROW,
            corner_radius=6,
            border_width=1,
            border_color=PurpleTheme.BORDER_HEADER,
            height=34,
        )
        self._header_label = customtkinter.CTkLabel(
            self,
            text=(
                f"{'TYPE':<12}{'CPU':<29}"
                f"{'RAM':>10}{'STORAGE':>12}{'DETAILS':>18}"
            ),
            font=("Cascadia Mono", 12),
            text_color=PurpleTheme.TEXT_MUTED,
            anchor="w",
        )
        self._header_label.grid(row=0, column=0, padx=12, pady=7, sticky="w")


class DeviceRowView(customtkinter.CTkFrame):
    """Visual row card displaying a single computer device."""

    def __init__(
        self,
        parent: customtkinter.CTkBaseClass,
        presenter: IDevicePresenter,
        is_even: bool,
    ) -> None:
        bg_color = PurpleTheme.BG_CARD_EVEN if is_even else PurpleTheme.BG_CARD_ODD
        super().__init__(
            parent,
            fg_color=bg_color,
            corner_radius=6,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
            height=38,
        )
        self._presenter = presenter
        self._render()

    def _render(self) -> None:
        self.grid_columnconfigure(0, weight=0, minsize=100)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=90)
        self.grid_columnconfigure(3, weight=0, minsize=110)
        self.grid_columnconfigure(4, weight=0, minsize=120)

        # 1. Type badge
        badge_text, badge_bg, badge_fg = self._presenter.type_badge
        badge = customtkinter.CTkLabel(
            self,
            text=badge_text,
            font=("Segoe UI", 11, "bold"),
            fg_color=badge_bg,
            text_color=badge_fg,
            corner_radius=4,
            width=80,
            height=24,
        )
        badge.grid(row=0, column=0, padx=(10, 6), pady=6)

        # 2. CPU label
        cpu_label = customtkinter.CTkLabel(
            self,
            text=self._presenter.cpu_text,
            font=("Segoe UI", 12, "bold"),
            text_color=PurpleTheme.TEXT_PRIMARY,
            anchor="w",
        )
        cpu_label.grid(row=0, column=1, padx=(12, 6), pady=6, sticky="ew")

        # 3. RAM label
        ram_label = customtkinter.CTkLabel(
            self,
            text=self._presenter.ram_text,
            font=("Segoe UI", 12),
            text_color=PurpleTheme.TEXT_ACCENT,
            anchor="center",
        )
        ram_label.grid(row=0, column=2, padx=6, pady=6, sticky="ew")

        # 4. Storage label
        storage_label = customtkinter.CTkLabel(
            self,
            text=self._presenter.storage_text,
            font=("Segoe UI", 12),
            text_color=PurpleTheme.TEXT_PRIMARY,
            anchor="center",
        )
        storage_label.grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        # 5. Extra details
        extra_label = customtkinter.CTkLabel(
            self,
            text=self._presenter.extra_text,
            font=("Segoe UI", 11),
            text_color=PurpleTheme.TEXT_SECONDARY,
            anchor="center",
        )
        extra_label.grid(row=0, column=4, padx=(6, 12), pady=6, sticky="ew")


class SortButtonBar(customtkinter.CTkFrame):
    """Grid container holding sort action buttons adhering to original row=1 layout."""

    def __init__(
        self,
        parent: customtkinter.CTkBaseClass,
        on_sort_selected: Callable[[ISortStrategy], None],
    ) -> None:
        super().__init__(
            parent,
            fg_color=PurpleTheme.BG_BUTTON_BAR,
            corner_radius=8,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
        )
        self._on_sort_selected = on_sort_selected
        self._buttons: dict[str, customtkinter.CTkButton] = {}
        self._strategies: list[ISortStrategy] = [
            CpuSortStrategy(),
            RamSortStrategy(),
            StorageSortStrategy(),
        ]
        self._create_buttons()

    def _create_buttons(self) -> None:
        self.grid_columnconfigure((0, 1, 2), weight=1)

        for col, strategy in enumerate(self._strategies):
            btn = customtkinter.CTkButton(
                self,
                text=f"Сортировка по {strategy.display_name}",
                command=lambda strat=strategy: self._on_sort_selected(strat),
                height=38,
                corner_radius=7,
                font=("Segoe UI", 12, "bold"),
                fg_color=PurpleTheme.BTN_DEFAULT_BG,
                hover_color=PurpleTheme.BTN_DEFAULT_HOVER,
                border_width=1,
                border_color=PurpleTheme.BORDER_SUBTLE,
            )
            btn.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
            self._buttons[strategy.key_name] = btn

    def update_active_state(
        self,
        active_key: Optional[str],
        direction: Optional[SortDirection],
    ) -> None:
        """Update button styles and direction arrows to indicate the active sort.

        Args:
            active_key: Key name of the active strategy, or None if unsorted.
            direction: Current SortDirection enum.
        """
        for strategy in self._strategies:
            btn = self._buttons[strategy.key_name]
            if strategy.key_name == active_key and direction is not None:
                btn.configure(
                    text=f"Сортировка по {strategy.display_name} {direction.arrow}",
                    fg_color=PurpleTheme.BTN_ACTIVE_BG,
                    hover_color=PurpleTheme.BTN_ACTIVE_HOVER,
                    border_color=PurpleTheme.BORDER_ACTIVE,
                )
            else:
                btn.configure(
                    text=f"Сортировка по {strategy.display_name}",
                    fg_color=PurpleTheme.BTN_DEFAULT_BG,
                    hover_color=PurpleTheme.BTN_DEFAULT_HOVER,
                    border_color=PurpleTheme.BORDER_SUBTLE,
                )


# ==============================================================================
# Main Application Controller
# ==============================================================================

class ComputerApp:
    """CustomTkinter application for displaying and sorting computers."""

    def __init__(self, computers: Sequence[Interface]) -> None:
        self._computers: list[Interface] = list(computers)
        self._active_strategy: Optional[ISortStrategy] = None
        self._current_direction: Optional[SortDirection] = None

        self._window = customtkinter.CTk()
        self._setup_window()
        self._create_layout()
        self._render_rows("Исходный порядок")

    def _setup_window(self) -> None:
        self._window.title("Lab 2 GUI - Computer Catalog")
        self._window.geometry("820x620")
        self._window.minsize(680, 460)
        self._window.configure(fg_color=PurpleTheme.BG_WINDOW)

    def _create_layout(self) -> None:
        # Original grid structure: row 0 = main content, row 1 = buttons
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
        main_container.grid_rowconfigure(0, weight=0)  # Header banner
        main_container.grid_rowconfigure(1, weight=0)  # Column headers
        main_container.grid_rowconfigure(2, weight=1)  # Scrollable list

        # 1. Header Banner
        self._header_banner = HeaderBannerView(main_container)
        self._header_banner.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        # 2. Table Column Headers
        self._table_header = TableHeaderView(main_container)
        self._table_header.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        # 3. Textbox keeps the whole catalog in one lightweight widget.
        self._device_textbox = customtkinter.CTkTextbox(
            main_container,
            height=420,
            fg_color=PurpleTheme.BG_CARD_CONTAINER,
            corner_radius=8,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
            font=("Cascadia Mono", 12),
            activate_scrollbars=True,
        )
        self._device_textbox.grid(row=2, column=0, sticky="nsew")
        self._device_textbox.tag_config("title", foreground=PurpleTheme.TEXT_ACCENT)
        self._device_textbox.tag_config("header", foreground=PurpleTheme.TEXT_PRIMARY)
        self._device_textbox.tag_config("separator", foreground=PurpleTheme.BORDER_HEADER)
        self._device_textbox.tag_config("pc", foreground=PurpleTheme.BADGE_PC_TEXT)
        self._device_textbox.tag_config("laptop", foreground=PurpleTheme.BADGE_LAPTOP_TEXT)
        self._device_textbox.tag_config("server", foreground=PurpleTheme.BADGE_SERVER_TEXT)
        self._device_textbox.configure(state="disabled")

        # Buttons Bar (Row 1, keeping the original layout grid)
        self._button_bar = SortButtonBar(
            self._window,
            on_sort_selected=self._handle_sort_request,
        )
        self._button_bar.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="ew")

    def _handle_sort_request(self, strategy: ISortStrategy) -> None:
        """Handle user clicking a sort button.

        Behavior:
        - First click on any column sorts from largest to smallest (DESCENDING).
        - Consecutive click on the SAME column toggles to ASCENDING.
        - Subsequent clicks toggle between DESCENDING and ASCENDING.
        """
        if self._active_strategy is None or self._active_strategy.key_name != strategy.key_name:
            # First click on this column: always descending (от большего к меньшему)
            self._active_strategy = strategy
            self._current_direction = SortDirection.DESCENDING
        else:
            # Consecutive click on the same column: toggle direction
            self._current_direction = self._current_direction.toggle()

        # Perform sort
        self._computers = self._active_strategy.sort(self._computers, self._current_direction)

        # Update button bar indicator
        self._button_bar.update_active_state(
            self._active_strategy.key_name,
            self._current_direction,
        )

        # Re-render device rows
        status_text = f"Сортировка: {strategy.display_name} ({self._current_direction.label}) {self._current_direction.arrow}"
        self._render_rows(status_text)

    def _render_rows(self, status_description: str) -> None:
        """Render all devices in one textbox instead of rebuilding widgets."""
        self._header_banner.update_status(len(self._computers), status_description)
        type_width = 12
        cpu_width = 29
        ram_width = 10
        storage_width = 12
        details_width = 18

        self._device_textbox.configure(state="normal")
        self._device_textbox.delete("1.0", "end")
        self._device_textbox.insert("end", f"{status_description}\n", "title")
        self._device_textbox.insert("end", "\n")
        self._device_textbox.insert(
            "end",
            "-" * (type_width + cpu_width + ram_width + storage_width + details_width) + "\n",
            "separator",
        )

        for device in self._computers:
            presenter = DevicePresenterFactory.create(device)
            type_name = presenter.type_badge[0]
            type_tag = type_name.lower()
            self._device_textbox.insert("end", f"{type_name:<{type_width}}", type_tag)
            self._device_textbox.insert(
                "end",
                f"{presenter.cpu_text:<{cpu_width}}"
                f"{presenter.ram_text:>{ram_width}}"
                f"{presenter.storage_text:>{storage_width}}"
                f"{presenter.extra_text:>{details_width}}\n",
            )
        self._device_textbox.configure(state="disabled")

    def run(self) -> None:
        """Start the CustomTkinter event loop."""
        self._window.mainloop()


# ==============================================================================
# Catalog Factory & Composition Root
# ==============================================================================

class ComputerCatalog:
    """Factory for the computer collection used by the laboratory GUI."""

    def create_devices(self) -> list[Interface]:
        """Instantiate and return standard list of laboratory devices."""
        devices: list[Interface] = []
        pc_cpus = [
            "Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9", "AMD Ryzen 3",
            "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9", "Intel Core i5-13400", "AMD Ryzen 5 5600X",
        ]
        for index in range(10):
            devices.append(PC(
                cpu=pc_cpus[index],
                ram=8 + (index % 4) * 8,
                storage=256 + index * 256,
                form_factor="Mini-ITX" if index % 2 == 0 else "ATX",
            ))

        laptop_cpus = [
            "Apple M1", "Apple M2", "Apple M3", "Intel Core i5-1240P", "Intel Core i7-12700H",
            "AMD Ryzen 7 6800U", "Intel Core Ultra 7", "AMD Ryzen 9 7940HS", "Apple M2 Pro", "Apple M3 Max",
        ]
        for index in range(10):
            devices.append(Laptop(
                cpu=laptop_cpus[index],
                ram=8 + (index % 3) * 8,
                storage=512 + (index % 4) * 512,
                battery_life=6 + index,
            ))

        server_cpus = [
            "AMD EPYC 7763", "AMD EPYC 9654", "Intel Xeon Silver 4314", "Intel Xeon Gold 6330", "Intel Xeon Platinum 8380",
            "AMD EPYC 7543", "Intel Xeon E-2388G", "AMD EPYC 9354", "Intel Xeon Gold 5418Y", "AMD EPYC 7713",
        ]
        for index in range(10):
            devices.append(Server(
                cpu=server_cpus[index],
                ram=32 + index * 32,
                storage=1000 + index * 2000,
                rack_units=1 + index % 4,
            ))
        return devices


class LaboratoryApplication:
    """Composition root for the object catalog and GUI."""

    def run(self) -> None:
        """Run the laboratory application."""
        ComputerApp(ComputerCatalog().create_devices()).run()


if __name__ == "__main__":
    LaboratoryApplication().run()
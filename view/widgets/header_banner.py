"""Header banner widget displaying title, item count status, and activity pulses."""

from __future__ import annotations

import customtkinter

from view.theme import PurpleTheme
from view.widgets.activity_indicator import ActivityIndicator
from view.widgets.status_ticker import StatusTicker


class HeaderBannerView(customtkinter.CTkFrame):
    """Application header banner containing title, badge counter, and status indicators."""

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        """Initialize header frame and layout widgets.

        Args:
            parent: Parent CustomTkinter container.
        """
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
            text_color="red",
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
        """Arrange banner components inside the grid."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        self._title_label.grid(row=0, column=0, padx=16, pady=10, sticky="w")
        self._status_badge.grid(row=0, column=1, padx=16, pady=10, sticky="e")
        self._activity_indicator.grid(row=0, column=2, padx=(0, 10), pady=0, sticky="e")
        self._status_ticker.grid(row=1, column=0, columnspan=3, padx=16, pady=(0, 8), sticky="ew")

    def update_status(self, total_count: int, order_description: str) -> None:
        """Update header status badge text with device count and order description.

        Args:
            total_count: Current count of devices in view.
            order_description: Descriptive title of active order.
        """
        self._status_badge.configure(text=f"{total_count} устройств • {order_description}")

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}()"

"""Fixed table header widget with aligned column titles."""

from __future__ import annotations

import customtkinter

from view.theme import PurpleTheme


class TableHeaderView(customtkinter.CTkFrame):
    """Header bar aligning monospace column names with tabular content below."""

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        """Initialize fixed table column header frame.

        Args:
            parent: Parent CustomTkinter container.
        """
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

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}()"

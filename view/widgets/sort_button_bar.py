"""Toolbar widget housing interactive sorting buttons."""

from __future__ import annotations

from typing import Callable, Dict, Optional, Tuple

import customtkinter

from view.theme import PurpleTheme


class SortButtonBar(customtkinter.CTkFrame):
    """Grid container holding sort action buttons dispatching callbacks on user clicks."""

    def __init__(
        self,
        parent: customtkinter.CTkBaseClass,
        on_sort_requested: Callable[[str], None],
    ) -> None:
        """Initialize button toolbar with sort options.

        Args:
            parent: Parent CustomTkinter container.
            on_sort_requested: Callback receiving strategy key ('cpu', 'ram', 'storage').
        """
        super().__init__(
            parent,
            fg_color=PurpleTheme.BG_BUTTON_BAR,
            corner_radius=8,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
        )
        self._on_sort_requested = on_sort_requested
        self._buttons: Dict[str, customtkinter.CTkButton] = {}

        # Definitions: (key, display_name)
        self._button_defs: Tuple[Tuple[str, str], ...] = (
            ("cpu", "CPU Power"),
            ("ram", "RAM"),
            ("storage", "Storage"),
        )
        self._create_buttons()

    def _create_buttons(self) -> None:
        """Instantiate and position CTkButtons within grid."""
        self.grid_columnconfigure((0, 1, 2), weight=1)

        for col, (key, display_name) in enumerate(self._button_defs):
            btn = customtkinter.CTkButton(
                self,
                text=f"Сортировка по {display_name}",
                command=lambda k=key: self._on_sort_requested(k),
                height=38,
                corner_radius=7,
                font=("Segoe UI", 12, "bold"),
                fg_color=PurpleTheme.BTN_DEFAULT_BG,
                hover_color=PurpleTheme.BTN_DEFAULT_HOVER,
                border_width=1,
                border_color=PurpleTheme.BORDER_SUBTLE,
            )
            btn.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
            self._buttons[key] = btn

    def update_active_state(
        self,
        active_key: Optional[str],
        direction_arrow: Optional[str],
    ) -> None:
        """Update button highlights and directional arrows to reflect the active sort.

        Args:
            active_key: Parameter key of the active sort, or None.
            direction_arrow: Direction indicator arrow character ('▲', '▼') or None.
        """
        for key, display_name in self._button_defs:
            btn = self._buttons.get(key)
            if btn is None:
                continue

            if key == active_key and direction_arrow:
                btn.configure(
                    text=f"Сортировка по {display_name} {direction_arrow}",
                    fg_color=PurpleTheme.BTN_ACTIVE_BG,
                    hover_color=PurpleTheme.BTN_ACTIVE_HOVER,
                    border_color=PurpleTheme.BORDER_ACTIVE,
                )
            else:
                btn.configure(
                    text=f"Сортировка по {display_name}",
                    fg_color=PurpleTheme.BTN_DEFAULT_BG,
                    hover_color=PurpleTheme.BTN_DEFAULT_HOVER,
                    border_color=PurpleTheme.BORDER_SUBTLE,
                )

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(total_buttons={len(self._buttons)})"

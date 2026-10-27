"""Toolbar of the chart window: metric selector and action buttons."""

from __future__ import annotations

from typing import Callable, Dict, Optional

import customtkinter

from view.theme import PurpleTheme


class ChartControlBar(customtkinter.CTkFrame):
    """Bottom control bar with metric switch, refresh, sort and close buttons."""

    def __init__(
        self,
        parent: customtkinter.CTkBaseClass,
        on_metric_selected: Callable[[str], None],
        on_refresh: Callable[[], None],
        on_sort: Callable[[], None],
        on_close: Callable[[], None],
    ) -> None:
        """Build control widgets.

        Args:
            parent: Parent container.
            on_metric_selected: Callback receiving selected metric key.
            on_refresh: Callback for reloading data from the model.
            on_sort: Callback for toggling chart sort order.
            on_close: Callback for closing the window.
        """
        super().__init__(
            parent,
            fg_color=PurpleTheme.BG_BUTTON_BAR,
            corner_radius=8,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
        )
        self._on_metric_selected = on_metric_selected
        self._title_to_key: Dict[str, str] = {}

        self.grid_columnconfigure((0, 1, 2), weight=1)

        self._metric_switch = customtkinter.CTkSegmentedButton(
            self,
            values=["-"],
            command=self._handle_metric_switch,
            font=("Segoe UI", 12, "bold"),
            selected_color=PurpleTheme.BTN_ACTIVE_BG,
            selected_hover_color=PurpleTheme.BTN_ACTIVE_HOVER,
            unselected_color=PurpleTheme.BTN_DEFAULT_BG,
            unselected_hover_color=PurpleTheme.BTN_DEFAULT_HOVER,
        )
        self._metric_switch.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 4), sticky="ew")

        self._refresh_button = self._make_button("Обновить данные", on_refresh)
        self._refresh_button.grid(row=1, column=0, padx=10, pady=(4, 10), sticky="ew")
        self._sort_button = self._make_button("Сортировать", on_sort)
        self._sort_button.grid(row=1, column=1, padx=10, pady=(4, 10), sticky="ew")
        self._close_button = self._make_button("Закрыть", on_close)
        self._close_button.grid(row=1, column=2, padx=10, pady=(4, 10), sticky="ew")

    def _make_button(self, text: str, command: Callable[[], None]) -> customtkinter.CTkButton:
        """Create a themed action button.

        Args:
            text: Button caption.
            command: Click callback.

        Returns:
            Configured ``CTkButton``.
        """
        return customtkinter.CTkButton(
            self,
            text=text,
            command=command,
            height=36,
            corner_radius=7,
            font=("Segoe UI", 12, "bold"),
            fg_color=PurpleTheme.BTN_DEFAULT_BG,
            hover_color=PurpleTheme.BTN_DEFAULT_HOVER,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
        )

    def set_metric_options(self, options: Dict[str, str], active_key: str) -> None:
        """Populate metric selector.

        Args:
            options: Mapping of metric key to display title.
            active_key: Key to preselect.
        """
        self._title_to_key = {title: key for key, title in options.items()}
        self._metric_switch.configure(values=list(options.values()))
        if active_key in options:
            self._metric_switch.set(options[active_key])

    def update_sort_state(self, arrow: Optional[str]) -> None:
        """Highlight sort button when ordering is active.

        Args:
            arrow: Direction arrow or None.
        """
        if arrow:
            self._sort_button.configure(text=f"Сортировать {arrow}", fg_color=PurpleTheme.BTN_ACTIVE_BG,
                                        hover_color=PurpleTheme.BTN_ACTIVE_HOVER,
                                        border_color=PurpleTheme.BORDER_ACTIVE)
        else:
            self._sort_button.configure(text="Сортировать", fg_color=PurpleTheme.BTN_DEFAULT_BG,
                                        hover_color=PurpleTheme.BTN_DEFAULT_HOVER,
                                        border_color=PurpleTheme.BORDER_SUBTLE)

    def _handle_metric_switch(self, title: str) -> None:
        """Translate selected title into metric key and notify listener."""
        key = self._title_to_key.get(title)
        if key is not None:
            self._on_metric_selected(key)

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(metrics={list(self._title_to_key.values())!r})"

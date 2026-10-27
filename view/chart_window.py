"""Separate top-level window (frame) hosting Matplotlib charts."""

from __future__ import annotations

from typing import Dict, Optional

import customtkinter

from presenter.chart_presenter_interface import IChartPresenter
from view.chart_view_interface import IChartView
from view.chart_view_model import ChartViewModel
from view.theme import PurpleTheme
from view.widgets.chart_canvas import ChartCanvas
from view.widgets.chart_control_bar import ChartControlBar


class ChartWindow(IChartView):
    """Passive chart frame: forwards every user action to ``IChartPresenter``."""

    def __init__(self, master: customtkinter.CTk) -> None:
        """Create the top-level window and its widgets.

        Args:
            master: Main application window.
        """
        self._presenter: Optional[IChartPresenter] = None
        self._window = customtkinter.CTkToplevel(master)
        self._window.title("Lab 4 - Графики каталога (Matplotlib)")
        self._window.geometry("820x640")
        self._window.minsize(620, 520)
        self._window.configure(fg_color=PurpleTheme.BG_WINDOW)
        self._window.protocol("WM_DELETE_WINDOW", self._handle_close)
        self._window.transient(master)
        self._build_layout()

    def _build_layout(self) -> None:
        """Arrange caption, chart canvas and control bar."""
        self._window.grid_columnconfigure(0, weight=1)
        self._window.grid_rowconfigure(1, weight=1)

        self._summary_label = customtkinter.CTkLabel(
            self._window,
            text="",
            font=("Segoe UI", 13, "bold"),
            text_color=PurpleTheme.TEXT_ACCENT,
            anchor="w",
        )
        self._summary_label.grid(row=0, column=0, padx=20, pady=(14, 4), sticky="ew")

        self._canvas = ChartCanvas(self._window)
        self._canvas.grid(row=1, column=0, padx=18, pady=(4, 10), sticky="nsew")

        self._controls = ChartControlBar(
            self._window,
            on_metric_selected=self._handle_metric_selected,
            on_refresh=self._handle_refresh,
            on_sort=self._handle_sort,
            on_close=self._handle_close,
        )
        self._controls.grid(row=2, column=0, padx=18, pady=(0, 18), sticky="ew")

    def set_presenter(self, presenter: IChartPresenter) -> None:
        """Bind chart presenter."""
        self._presenter = presenter

    def set_metric_options(self, options: Dict[str, str], active_key: str) -> None:
        """Populate metric selector."""
        self._controls.set_metric_options(options, active_key)

    def render_chart(self, chart: ChartViewModel) -> None:
        """Draw chart and update caption."""
        self._summary_label.configure(text=chart.summary_text, text_color=PurpleTheme.TEXT_ACCENT)
        self._canvas.draw_chart(chart)

    def update_sort_state(self, arrow: Optional[str]) -> None:
        """Reflect sort state on the toolbar."""
        self._controls.update_sort_state(arrow)

    def show_error(self, message: str) -> None:
        """Show error in caption."""
        self._summary_label.configure(text=f"ОШИБКА: {message}", text_color=PurpleTheme.BADGE_LAPTOP_TEXT)

    def is_open(self) -> bool:
        """Return True while the Tk window exists."""
        try:
            return bool(self._window.winfo_exists())
        except Exception:
            return False

    def focus(self) -> None:
        """Bring window to front."""
        self._window.deiconify()
        self._window.lift()
        self._window.focus_force()

    def close(self) -> None:
        """Destroy the window."""
        if self.is_open():
            self._window.destroy()

    def _handle_metric_selected(self, key: str) -> None:
        """Forward metric switch to presenter."""
        if self._presenter is not None:
            self._presenter.handle_metric_selected(key)

    def _handle_refresh(self) -> None:
        """Forward refresh click to presenter."""
        if self._presenter is not None:
            self._presenter.handle_refresh_requested()

    def _handle_sort(self) -> None:
        """Forward sort click to presenter."""
        if self._presenter is not None:
            self._presenter.handle_sort_requested()

    def _handle_close(self) -> None:
        """Forward close request to presenter (or close directly if unbound)."""
        if self._presenter is not None:
            self._presenter.handle_close_requested()
        else:
            self.close()

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(open={self.is_open()})"

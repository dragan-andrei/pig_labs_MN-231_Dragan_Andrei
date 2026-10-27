"""CustomTkinter frame embedding a Matplotlib figure."""

from __future__ import annotations

from typing import List

import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Patch

from view.chart_view_model import ChartViewModel
from view.theme import PurpleTheme


class ChartCanvas(customtkinter.CTkFrame):
    """Adapter widget bridging Matplotlib ``Figure`` into the CustomTkinter layout.

    Uses the object-oriented Matplotlib API (``Figure``) instead of ``pyplot``
    so that no global plotting state is shared between windows.
    """

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        """Create figure, axes and Tk canvas.

        Args:
            parent: Parent CustomTkinter container.
        """
        super().__init__(
            parent,
            fg_color=PurpleTheme.CHART_FIGURE_BG,
            corner_radius=8,
            border_width=1,
            border_color=PurpleTheme.BORDER_SUBTLE,
        )
        self._figure = Figure(figsize=(7.2, 4.4), dpi=100, facecolor=PurpleTheme.CHART_FIGURE_BG)
        self._axes = self._figure.add_subplot(111)
        self._figure_canvas = FigureCanvasTkAgg(self._figure, master=self)
        self._figure_canvas.get_tk_widget().configure(bg=PurpleTheme.CHART_FIGURE_BG, highlightthickness=0)
        self._figure_canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

    def draw_chart(self, chart: ChartViewModel) -> None:
        """Render a bar chart from the presentation model.

        Args:
            chart: Prepared chart description.
        """
        axes = self._axes
        axes.clear()
        self._style_axes()

        title = f"{chart.title} {chart.sort_arrow}" if chart.sort_arrow else chart.title
        axes.set_title(title, color=PurpleTheme.TEXT_PRIMARY, fontsize=13, fontweight="bold", pad=12)
        axes.set_ylabel(chart.y_label, color=PurpleTheme.TEXT_SECONDARY)

        if chart.is_empty:
            axes.text(0.5, 0.5, "Нет данных", ha="center", va="center",
                      color=PurpleTheme.TEXT_MUTED, transform=axes.transAxes, fontsize=14)
            self._figure_canvas.draw_idle()
            return

        positions: List[int] = list(range(len(chart.values)))
        bars = axes.bar(positions, chart.values, color=chart.bar_colors,
                        edgecolor=PurpleTheme.BORDER_HEADER, linewidth=1, zorder=3, width=0.7)
        dense = len(chart.values) > 15
        axes.bar_label(bars, labels=[self._compact(v) for v in chart.values], padding=3,
                       color=PurpleTheme.TEXT_SECONDARY, fontsize=7 if dense else 8,
                       rotation=90 if dense else 0)
        axes.axhline(chart.average, color=PurpleTheme.CHART_AVERAGE_LINE, linestyle="--",
                     linewidth=1.3, zorder=4, label=f"Среднее: {chart.average:.1f}")

        axes.set_xticks(positions)
        axes.set_xticklabels(chart.labels, rotation=40, ha="right", fontsize=8)
        axes.set_ylim(0, max(chart.values) * 1.15 or 1)

        handles = [Patch(facecolor=color, label=name) for name, color in chart.legend]
        handles.extend(axes.get_legend_handles_labels()[0])
        legend = axes.legend(handles=handles, loc="upper right", fontsize=8, framealpha=0.85,
                             facecolor=PurpleTheme.BG_HEADER_ROW, edgecolor=PurpleTheme.BORDER_HEADER)
        for text in legend.get_texts():
            text.set_color(PurpleTheme.TEXT_PRIMARY)

        self._figure.tight_layout()
        self._figure_canvas.draw_idle()

    @staticmethod
    def _compact(value: float) -> str:
        """Format a number compactly (e.g. 96000 -> '96k').

        Args:
            value: Number to format.

        Returns:
            Short textual representation.
        """
        return f"{value / 1000:g}k" if value >= 10000 else f"{value:g}"

    def _style_axes(self) -> None:
        """Apply purple dark theme to axes, ticks, spines and grid."""
        axes = self._axes
        axes.set_facecolor(PurpleTheme.CHART_AXES_BG)
        axes.tick_params(colors=PurpleTheme.TEXT_SECONDARY)
        for side, spine in axes.spines.items():
            spine.set_visible(side in ("left", "bottom"))
            spine.set_color(PurpleTheme.BORDER_HEADER)
        axes.grid(axis="y", color=PurpleTheme.CHART_GRID, linestyle="-", linewidth=0.7, zorder=0)

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(figure={self._figure!r})"

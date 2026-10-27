"""Presentation DTO describing a ready-to-draw bar chart."""

from __future__ import annotations

from typing import Optional, Tuple


class ChartViewModel:
    """Immutable, fully formatted chart description consumed by the chart view."""

    def __init__(
        self,
        title: str,
        y_label: str,
        labels: Tuple[str, ...],
        values: Tuple[float, ...],
        bar_colors: Tuple[str, ...],
        average: float,
        summary_text: str,
        legend: Tuple[Tuple[str, str], ...] = (),
        sort_arrow: Optional[str] = None,
    ) -> None:
        """Initialize chart presentation model.

        Args:
            title: Chart title.
            y_label: Y axis caption.
            labels: X axis tick labels.
            values: Bar heights.
            bar_colors: Hex color per bar.
            average: Mean value drawn as reference line.
            summary_text: Short statistics caption.
            legend: Pairs of (category name, hex color).
            sort_arrow: Active sort arrow or None.
        """
        self._title = title
        self._y_label = y_label
        self._labels = tuple(labels)
        self._values = tuple(values)
        self._bar_colors = tuple(bar_colors)
        self._average = float(average)
        self._summary_text = summary_text
        self._legend = tuple(legend)
        self._sort_arrow = sort_arrow

    @property
    def title(self) -> str:
        """Return chart title."""
        return self._title

    @property
    def y_label(self) -> str:
        """Return Y axis caption."""
        return self._y_label

    @property
    def labels(self) -> Tuple[str, ...]:
        """Return X axis labels."""
        return self._labels

    @property
    def values(self) -> Tuple[float, ...]:
        """Return bar heights."""
        return self._values

    @property
    def bar_colors(self) -> Tuple[str, ...]:
        """Return bar colors."""
        return self._bar_colors

    @property
    def average(self) -> float:
        """Return average reference value."""
        return self._average

    @property
    def summary_text(self) -> str:
        """Return statistics caption."""
        return self._summary_text

    @property
    def legend(self) -> Tuple[Tuple[str, str], ...]:
        """Return legend entries."""
        return self._legend

    @property
    def sort_arrow(self) -> Optional[str]:
        """Return active sort arrow."""
        return self._sort_arrow

    @property
    def is_empty(self) -> bool:
        """Return True when there is nothing to draw."""
        return not self._values

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(title={self._title!r}, bars={len(self._values)})"

    def __str__(self) -> str:
        """Return human-readable representation."""
        return f"{self._title}: {self._summary_text}"

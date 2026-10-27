"""Immutable value object describing a plottable data series."""

from __future__ import annotations

from typing import Optional, Tuple

from model.exceptions import ChartDataError
from model.sorting.direction import SortDirection


class ChartSeries:
    """Immutable labelled numeric series produced by the model for charting.

    Invariants:
        ``labels``, ``values`` and ``categories`` always have equal length.
    """

    def __init__(
        self,
        metric_key: str,
        title: str,
        unit: str,
        labels: Tuple[str, ...],
        values: Tuple[float, ...],
        categories: Tuple[str, ...],
        direction: Optional[SortDirection] = None,
    ) -> None:
        """Initialize series and validate its consistency.

        Args:
            metric_key: Identifier of the metric that produced the values.
            title: Human-readable series title.
            unit: Measurement unit.
            labels: X-axis labels (one per device).
            values: Numeric values (one per device).
            categories: Device type names used for colouring.
            direction: Sort direction applied, or None for catalog order.

        Raises:
            ChartDataError: If tuple lengths differ or values are negative.
        """
        if not (len(labels) == len(values) == len(categories)):
            raise ChartDataError("Labels, values and categories must have equal length.")
        if any(value < 0 for value in values):
            raise ChartDataError("Chart values must be non-negative.")
        self._metric_key = metric_key
        self._title = title
        self._unit = unit
        self._labels = tuple(labels)
        self._values = tuple(float(v) for v in values)
        self._categories = tuple(categories)
        self._direction = direction

    @property
    def metric_key(self) -> str:
        """Return metric identifier."""
        return self._metric_key

    @property
    def title(self) -> str:
        """Return series title."""
        return self._title

    @property
    def unit(self) -> str:
        """Return measurement unit."""
        return self._unit

    @property
    def labels(self) -> Tuple[str, ...]:
        """Return X-axis labels."""
        return self._labels

    @property
    def values(self) -> Tuple[float, ...]:
        """Return numeric values."""
        return self._values

    @property
    def categories(self) -> Tuple[str, ...]:
        """Return device category per point."""
        return self._categories

    @property
    def direction(self) -> Optional[SortDirection]:
        """Return applied sort direction, if any."""
        return self._direction

    @property
    def average(self) -> float:
        """Return arithmetic mean of values (0 for empty series)."""
        return sum(self._values) / len(self._values) if self._values else 0.0

    @property
    def maximum(self) -> float:
        """Return maximum value (0 for empty series)."""
        return max(self._values, default=0.0)

    def sorted_by(self, direction: SortDirection) -> ChartSeries:
        """Return a new series ordered by value.

        Args:
            direction: Ordering direction.

        Returns:
            New sorted ``ChartSeries`` instance.
        """
        points = sorted(
            zip(self._labels, self._values, self._categories),
            key=lambda point: point[1],
            reverse=(direction == SortDirection.DESCENDING),
        )
        return ChartSeries(
            metric_key=self._metric_key,
            title=self._title,
            unit=self._unit,
            labels=tuple(p[0] for p in points),
            values=tuple(p[1] for p in points),
            categories=tuple(p[2] for p in points),
            direction=direction,
        )

    def __len__(self) -> int:
        """Return number of points."""
        return len(self._values)

    def __eq__(self, other: object) -> bool:
        """Compare series by full content."""
        if not isinstance(other, ChartSeries):
            return NotImplemented
        return (
            self._metric_key, self._labels, self._values, self._categories, self._direction
        ) == (other._metric_key, other._labels, other._values, other._categories, other._direction)

    def __hash__(self) -> int:
        """Hash based on immutable content."""
        return hash((self._metric_key, self._labels, self._values, self._categories, self._direction))

    def __repr__(self) -> str:
        """Return developer representation."""
        return (
            f"{self.__class__.__name__}(metric={self._metric_key!r}, "
            f"points={len(self)}, direction={self._direction!r})"
        )

    def __str__(self) -> str:
        """Return human-readable representation."""
        return f"{self._title}: {len(self)} точек, среднее {self.average:.1f} {self._unit}"

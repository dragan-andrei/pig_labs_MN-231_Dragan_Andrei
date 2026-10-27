"""Service building chart series from device collections."""

from __future__ import annotations

from typing import Dict, Optional, Sequence

from model.charting.chart_metric import IChartMetric
from model.charting.chart_series import ChartSeries
from model.charting.cpu_metric import CpuChartMetric
from model.charting.ram_metric import RamChartMetric
from model.charting.storage_metric import StorageChartMetric
from model.exceptions import ChartDataError
from model.interface import Interface
from model.sorting.direction import SortDirection


class ChartSeriesBuilder:
    """Transforms device sequences into ``ChartSeries`` using registered metrics.

    Open/Closed: new metrics are added via ``register`` without modifying this class.
    """

    def __init__(self) -> None:
        """Initialize builder with default CPU, RAM and storage metrics."""
        self._metrics: Dict[str, IChartMetric] = {}
        for metric in (CpuChartMetric(), RamChartMetric(), StorageChartMetric()):
            self.register(metric)

    def register(self, metric: IChartMetric) -> None:
        """Register an additional metric.

        Args:
            metric: Metric strategy instance.

        Raises:
            ChartDataError: If metric is invalid.
        """
        if not isinstance(metric, IChartMetric):
            raise ChartDataError("Only IChartMetric instances can be registered.")
        self._metrics[metric.key_name] = metric

    def get_metric_titles(self) -> Dict[str, str]:
        """Return mapping of metric key to display title."""
        return {key: metric.display_name for key, metric in self._metrics.items()}

    def build(
        self,
        devices: Sequence[Interface],
        metric_key: str,
        direction: Optional[SortDirection] = None,
    ) -> ChartSeries:
        """Build a series for the given devices and metric.

        Args:
            devices: Devices in catalog order.
            metric_key: Registered metric identifier.
            direction: Optional ordering of the produced series.

        Returns:
            Constructed ``ChartSeries``.

        Raises:
            ChartDataError: If the metric key is unknown.
        """
        metric = self._metrics.get(metric_key)
        if metric is None:
            raise ChartDataError(f"Chart metric '{metric_key}' is not recognized.")

        categories = tuple(device.__class__.__name__ for device in devices)
        series = ChartSeries(
            metric_key=metric.key_name,
            title=metric.display_name,
            unit=metric.unit,
            labels=tuple(f"{category} #{i}" for i, category in enumerate(categories, start=1)),
            values=tuple(metric.measure(device) for device in devices),
            categories=categories,
        )
        return series.sorted_by(direction) if direction is not None else series

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(metrics={list(self._metrics)!r})"

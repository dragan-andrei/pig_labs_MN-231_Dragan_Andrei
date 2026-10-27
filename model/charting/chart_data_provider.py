"""Role interface for models capable of supplying chart data."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional

from model.charting.chart_series import ChartSeries
from model.sorting.direction import SortDirection


class IChartDataProvider(ABC):
    """Segregated contract (ISP) exposing only chart-related model operations."""

    @abstractmethod
    def get_chart_metrics(self) -> Dict[str, str]:
        """Return mapping of available chart metric keys to display titles."""

    @abstractmethod
    def get_chart_series(
        self,
        metric_key: str,
        direction: Optional[SortDirection] = None,
    ) -> ChartSeries:
        """Build a chart series from the current catalog.

        Args:
            metric_key: Metric identifier ('cpu', 'ram', 'storage').
            direction: Optional ordering of chart points.

        Returns:
            Ready-to-plot ``ChartSeries``.

        Raises:
            ChartDataError: If the metric is unknown or data is invalid.
        """

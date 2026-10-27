"""Chart metric for processor benchmark power."""

from __future__ import annotations

from model.charting.chart_metric import IChartMetric
from model.interface import Interface
from model.sorting.cpu_catalog import CpuPowerCatalog


class CpuChartMetric(IChartMetric):
    """Plots CPU benchmark score resolved through ``CpuPowerCatalog``."""

    @property
    def key_name(self) -> str:
        """Return metric identifier."""
        return "cpu"

    @property
    def display_name(self) -> str:
        """Return human-readable metric title."""
        return "CPU Power"

    @property
    def unit(self) -> str:
        """Return measurement unit."""
        return "pts"

    def measure(self, device: Interface) -> float:
        """Return benchmark score of the device processor.

        Args:
            device: Device entity to measure.

        Returns:
            Benchmark score (0 for unknown CPU models).
        """
        return float(CpuPowerCatalog.score_for(device.get_parameter(self.key_name)))

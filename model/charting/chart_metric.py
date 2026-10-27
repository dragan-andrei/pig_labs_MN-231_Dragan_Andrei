"""Abstract contract for numeric metrics that can be plotted on a chart."""

from __future__ import annotations

from abc import ABC, abstractmethod

from model.interface import Interface


class IChartMetric(ABC):
    """Strategy contract extracting a single numeric value from a device for charting.

    Invariants:
        ``key_name`` is unique among registered metrics and ``measure`` never
        returns a negative number.
    """

    @property
    @abstractmethod
    def key_name(self) -> str:
        """Return unique metric identifier (e.g. 'cpu', 'ram', 'storage')."""

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Return human-readable metric title."""

    @property
    @abstractmethod
    def unit(self) -> str:
        """Return measurement unit shown on the Y axis."""

    @abstractmethod
    def measure(self, device: Interface) -> float:
        """Extract the numeric metric value from a device.

        Args:
            device: Device entity to measure.

        Returns:
            Non-negative numeric value.

        Raises:
            ChartDataError: If the value cannot be extracted.
        """

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(key={self.key_name!r})"

    def __str__(self) -> str:
        """Return human-readable representation."""
        return f"{self.display_name} ({self.unit})"

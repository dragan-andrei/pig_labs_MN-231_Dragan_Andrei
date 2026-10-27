"""Reusable metric reading a positive integer device parameter."""

from __future__ import annotations

from model.charting.chart_metric import IChartMetric
from model.exceptions import ChartDataError
from model.interface import Interface


class IntegerParameterMetric(IChartMetric):
    """Base metric that reads an integer parameter (RAM, storage) from a device."""

    def __init__(self, key_name: str, display_name: str, unit: str) -> None:
        """Initialize metric descriptor.

        Args:
            key_name: Device parameter key to read.
            display_name: Human-readable metric title.
            unit: Measurement unit label.

        Raises:
            ChartDataError: If any descriptor is empty.
        """
        for value in (key_name, display_name, unit):
            if not isinstance(value, str) or not value.strip():
                raise ChartDataError("Metric descriptors must be non-empty strings.")
        self._key_name = key_name
        self._display_name = display_name
        self._unit = unit

    @property
    def key_name(self) -> str:
        """Return parameter identifier."""
        return self._key_name

    @property
    def display_name(self) -> str:
        """Return human-readable metric title."""
        return self._display_name

    @property
    def unit(self) -> str:
        """Return measurement unit."""
        return self._unit

    def measure(self, device: Interface) -> float:
        """Read the integer parameter from the device.

        Args:
            device: Device entity to measure.

        Returns:
            Parameter value as float.

        Raises:
            ChartDataError: If the parameter is not numeric.
        """
        try:
            return float(int(device.get_parameter(self._key_name) or 0))
        except (TypeError, ValueError) as err:
            raise ChartDataError(f"Parameter '{self._key_name}' is not numeric: {err}") from err

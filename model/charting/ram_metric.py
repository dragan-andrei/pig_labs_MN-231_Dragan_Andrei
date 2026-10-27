"""Chart metric for RAM capacity."""

from __future__ import annotations

from model.charting.integer_parameter_metric import IntegerParameterMetric


class RamChartMetric(IntegerParameterMetric):
    """Plots device RAM capacity in gigabytes."""

    def __init__(self) -> None:
        """Initialize RAM metric descriptor."""
        super().__init__(key_name="ram", display_name="RAM", unit="GB")

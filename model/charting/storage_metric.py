"""Chart metric for storage capacity."""

from __future__ import annotations

from model.charting.integer_parameter_metric import IntegerParameterMetric


class StorageChartMetric(IntegerParameterMetric):
    """Plots device storage capacity in gigabytes."""

    def __init__(self) -> None:
        """Initialize storage metric descriptor."""
        super().__init__(key_name="storage", display_name="Storage", unit="GB")

"""Contract for the presenter driving the chart frame."""

from __future__ import annotations

from abc import ABC, abstractmethod


class IChartPresenter(ABC):
    """Mediates between ``IChartDataProvider`` (model) and ``IChartView``."""

    @abstractmethod
    def initialize(self) -> None:
        """Populate view with metric options and draw the first chart."""

    @abstractmethod
    def handle_metric_selected(self, metric_key: str) -> None:
        """Switch plotted metric.

        Args:
            metric_key: Metric identifier selected by the user.
        """

    @abstractmethod
    def handle_refresh_requested(self) -> None:
        """Reload chart data from the model."""

    @abstractmethod
    def handle_sort_requested(self) -> None:
        """Cycle chart ordering: catalog -> descending -> ascending -> catalog."""

    @abstractmethod
    def handle_close_requested(self) -> None:
        """Close the chart view."""

    @abstractmethod
    def is_active(self) -> bool:
        """Return True while the bound chart view is open."""

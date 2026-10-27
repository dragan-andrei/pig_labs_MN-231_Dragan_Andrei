"""Abstract contract for the chart frame view."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Optional

from view.chart_view_model import ChartViewModel

if TYPE_CHECKING:
    from presenter.chart_presenter_interface import IChartPresenter


class IChartView(ABC):
    """Passive view contract for the separate chart window."""

    @abstractmethod
    def set_presenter(self, presenter: IChartPresenter) -> None:
        """Bind chart presenter receiving user actions.

        Args:
            presenter: Chart presenter instance.
        """

    @abstractmethod
    def set_metric_options(self, options: Dict[str, str], active_key: str) -> None:
        """Populate metric selector.

        Args:
            options: Mapping of metric key to display title.
            active_key: Currently selected metric key.
        """

    @abstractmethod
    def render_chart(self, chart: ChartViewModel) -> None:
        """Draw the chart described by the view model.

        Args:
            chart: Prepared chart presentation model.
        """

    @abstractmethod
    def update_sort_state(self, arrow: Optional[str]) -> None:
        """Reflect current chart sort direction on the sort button.

        Args:
            arrow: Direction arrow or None for catalog order.
        """

    @abstractmethod
    def show_error(self, message: str) -> None:
        """Display an error message inside the chart frame.

        Args:
            message: Error description.
        """

    @abstractmethod
    def is_open(self) -> bool:
        """Return True while the chart window exists."""

    @abstractmethod
    def focus(self) -> None:
        """Bring the chart window to the front."""

    @abstractmethod
    def close(self) -> None:
        """Destroy the chart window."""

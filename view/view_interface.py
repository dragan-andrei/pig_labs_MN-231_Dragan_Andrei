"""Abstract contract defining the Computer View interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Sequence

from view.chart_view_interface import IChartView
from view.view_model import DeviceViewModel

if TYPE_CHECKING:
    from presenter.presenter_interface import IComputerPresenter


class IComputerView(ABC):
    """Abstract interface defining the contract that GUI views must satisfy."""

    @abstractmethod
    def set_presenter(self, presenter: IComputerPresenter) -> None:
        """Bind presenter to the view for event callbacks.

        Args:
            presenter: An IComputerPresenter instance.
        """

    @abstractmethod
    def display_devices(
        self,
        devices: Sequence[DeviceViewModel],
        status_description: str,
        total_count: int,
    ) -> None:
        """Render device presentation items and update status description.

        Args:
            devices: Sequence of pre-formatted device presentation models.
            status_description: Human-readable text indicating current sort state.
            total_count: Total count of devices displayed.
        """

    @abstractmethod
    def update_sort_button_state(
        self,
        active_key: Optional[str],
        direction_arrow: Optional[str],
    ) -> None:
        """Update button active states and directional indicators.

        Args:
            active_key: Strategy parameter key that is currently active, or None.
            direction_arrow: Arrow character ('▲' or '▼') or None.
        """

    @abstractmethod
    def show_error(self, message: str) -> None:
        """Display error alert or banner to the user.

        Args:
            message: Descriptive error message.
        """

    @abstractmethod
    def open_chart_view(self) -> IChartView:
        """Create the separate chart frame and return it as an abstraction."""

    @abstractmethod
    def focus_chart_view(self) -> None:
        """Bring an already opened chart frame to the front."""

    @abstractmethod
    def start(self) -> None:
        """Start the GUI event processing loop."""

    @abstractmethod
    def close(self) -> None:
        """Terminate the GUI window."""

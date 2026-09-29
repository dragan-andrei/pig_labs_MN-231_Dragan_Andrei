"""Concrete ComputerPresenter coordinating catalog model data and graphic view."""

from __future__ import annotations

from typing import List

from model.exceptions import DomainError
from model.interface import Interface
from model.model_interface import IComputerModel
from presenter.adapters.presenter_factory import DevicePresenterFactory
from presenter.presenter_interface import IComputerPresenter
from view.view_interface import IComputerView
from view.view_model import DeviceViewModel


class ComputerPresenter(IComputerPresenter):
    """Coordinates business logic in IComputerModel with graphical interactions in IComputerView."""

    def __init__(self, model: IComputerModel, view: IComputerView) -> None:
        """Initialize presenter with model and view dependencies.

        Args:
            model: Data storage and processing model abstraction.
            view: Graphic presentation view abstraction.
        """
        self._model = model
        self._view = view

    def initialize(self) -> None:
        """Load initial device state from model and render onto view."""
        self._update_view_from_model()

    def handle_sort_requested(self, key_name: str) -> None:
        """Process sorting request triggered by view button callback.

        Calls model sorting methods, transforms resulting entities into view models,
        and triggers view re-render with updated button styling.

        Args:
            key_name: Attribute key ('cpu', 'ram', 'storage') requested for ordering.
        """
        try:
            self._model.sort_by_strategy_key(key_name)
            self._update_view_from_model()
        except DomainError as err:
            self._view.show_error(f"Ошибка сортировки: {err}")

    def handle_reset_requested(self) -> None:
        """Reset model to original device ordering and refresh view."""
        try:
            self._model.reset()
            self._update_view_from_model()
        except DomainError as err:
            self._view.show_error(f"Ошибка сброса: {err}")

    def _update_view_from_model(self) -> None:
        """Helper to transform model state into view models and notify view."""
        devices = self._model.get_devices()
        view_models: List[DeviceViewModel] = [
            DevicePresenterFactory.create(device).to_view_model()
            for device in devices
        ]

        active_strategy = self._model.get_active_strategy()
        direction = self._model.get_current_direction()

        active_key = active_strategy.key_name if active_strategy else None
        direction_arrow = direction.arrow if direction else None

        self._view.display_devices(
            devices=view_models,
            status_description=self._model.get_status_description(),
            total_count=self._model.get_device_count(),
        )
        self._view.update_sort_button_state(
            active_key=active_key,
            direction_arrow=direction_arrow,
        )

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(model={self._model!r}, view={self._view!r})"

"""Contract for the Computer Presenter coordinating Model and View."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class IComputerPresenter(ABC):
    """Abstract contract for presenters mediating between catalog model and view."""

    @abstractmethod
    def initialize(self) -> None:
        """Fetch initial dataset from model, transform to view models, and bind view."""

    @abstractmethod
    def handle_sort_requested(self, key_name: str) -> None:
        """Handle sorting request triggered by user interaction in the view.

        Args:
            key_name: Attribute key ('cpu', 'ram', 'storage') requested for ordering.
        """

    @abstractmethod
    def handle_reset_requested(self) -> None:
        """Handle reset request to return data to initial sequence."""

    @abstractmethod
    def handle_add_requested(self, device_type: str, values: Dict[str, Any]) -> None:
        """Handle creation of a device submitted by the view."""

    @abstractmethod
    def handle_edit_requested(self, index: int, device_type: str, values: Dict[str, Any]) -> None:
        """Handle replacement of an existing device submitted by the view."""

    @abstractmethod
    def handle_delete_requested(self, index: int) -> None:
        """Handle deletion of a device requested by the view."""

    @abstractmethod
    def handle_chart_requested(self) -> None:
        """Handle opening of the separate chart frame."""

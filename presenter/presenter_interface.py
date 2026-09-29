"""Contract for the Computer Presenter coordinating Model and View."""

from __future__ import annotations

from abc import ABC, abstractmethod


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

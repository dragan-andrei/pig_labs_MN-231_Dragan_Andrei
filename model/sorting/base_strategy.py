"""Abstract base strategy contract for computer device sorting."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from model.interface import Interface
from model.sorting.direction import SortDirection


class ISortStrategy(ABC):
    """Contract for sorting collections of computer devices."""

    @property
    @abstractmethod
    def key_name(self) -> str:
        """Return internal parameter key used for extraction."""

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Return human-readable strategy title."""

    @abstractmethod
    def sort(self, items: List[Interface], direction: SortDirection) -> List[Interface]:
        """Sort the given list of devices according to strategy rules.

        Args:
            items: The list of devices to sort.
            direction: SortDirection specifying ascending or descending order.

        Returns:
            The sorted list of devices.

        Raises:
            SortStrategyError: If an error occurs during comparison or extraction.
        """

    @abstractmethod
    def __repr__(self) -> str:
        """Return developer representation."""

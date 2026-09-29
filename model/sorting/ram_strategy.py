"""Sorting strategy based on RAM capacity in gigabytes."""

from __future__ import annotations

from typing import List

from model.exceptions import SortStrategyError
from model.interface import Interface
from model.sorting.base_strategy import ISortStrategy
from model.sorting.direction import SortDirection


class RamSortStrategy(ISortStrategy):
    """Sorts computer devices based on memory capacity in gigabytes."""

    @property
    def key_name(self) -> str:
        """Return parameter identifier."""
        return "ram"

    @property
    def display_name(self) -> str:
        """Return human-readable strategy name."""
        return "RAM"

    def sort(self, items: List[Interface], direction: SortDirection) -> List[Interface]:
        """Sort devices by RAM capacity.

        Args:
            items: List of computer entities.
            direction: SortDirection order.

        Returns:
            Sorted list of computer entities.

        Raises:
            SortStrategyError: If sorting fails.
        """
        try:
            return sorted(
                items,
                key=lambda item: int(item.get_parameter(self.key_name) or 0),
                reverse=(direction == SortDirection.DESCENDING),
            )
        except Exception as err:
            raise SortStrategyError(f"Failed to sort devices by RAM: {err}") from err

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(key={self.key_name!r})"

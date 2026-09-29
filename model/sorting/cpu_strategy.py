"""Sorting strategy based on processor performance benchmark scores."""

from __future__ import annotations

from typing import List

from model.exceptions import SortStrategyError
from model.interface import Interface
from model.sorting.base_strategy import ISortStrategy
from model.sorting.cpu_catalog import CpuPowerCatalog
from model.sorting.direction import SortDirection


class CpuSortStrategy(ISortStrategy):
    """Sorts computer devices based on CPU computational power benchmark."""

    @property
    def key_name(self) -> str:
        """Return parameter identifier."""
        return "cpu"

    @property
    def display_name(self) -> str:
        """Return human-readable strategy name."""
        return "CPU Power"

    def sort(self, items: List[Interface], direction: SortDirection) -> List[Interface]:
        """Sort devices by processor performance.

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
                key=lambda item: CpuPowerCatalog.score_for(item.get_parameter(self.key_name)),
                reverse=(direction == SortDirection.DESCENDING),
            )
        except Exception as err:
            raise SortStrategyError(f"Failed to sort devices by CPU: {err}") from err

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(key={self.key_name!r})"

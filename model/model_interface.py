"""Interface contract defining the Computer Model abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Sequence, Tuple

from model.interface import Interface
from model.sorting.base_strategy import ISortStrategy
from model.sorting.direction import SortDirection


class IComputerModel(ABC):
    """Abstract contract for computer data storage, retrieval, and sorting."""

    @abstractmethod
    def get_devices(self) -> Sequence[Interface]:
        """Return the sequence of stored computer entities."""

    @abstractmethod
    def get_device_count(self) -> int:
        """Return the total number of managed devices."""

    @abstractmethod
    def get_active_strategy(self) -> Optional[ISortStrategy]:
        """Return currently active sorting strategy, if any."""

    @abstractmethod
    def get_current_direction(self) -> Optional[SortDirection]:
        """Return current sorting direction, if any."""

    @abstractmethod
    def get_status_description(self) -> str:
        """Return descriptive text representation of current state/sorting."""

    @abstractmethod
    def sort_by_strategy_key(self, key_name: str) -> Tuple[Sequence[Interface], str]:
        """Sort devices using registered strategy matching the key name.

        Args:
            key_name: Parameter key identifying the sort strategy (e.g., 'cpu', 'ram', 'storage').

        Returns:
            Tuple containing the newly sorted device sequence and status text.

        Raises:
            ModelError: If strategy key is unknown or sorting fails.
        """

    @abstractmethod
    def get_available_strategies(self) -> Dict[str, ISortStrategy]:
        """Return mapping of available sort strategies keyed by parameter name."""

    @abstractmethod
    def reset(self) -> None:
        """Reset devices back to original initial dataset ordering."""

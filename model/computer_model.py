"""Concrete ComputerModel managing device collection state and business logic."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

from model.exceptions import ModelError, SortStrategyError
from model.interface import Interface
from model.model_interface import IComputerModel
from model.sorting.base_strategy import ISortStrategy
from model.sorting.cpu_strategy import CpuSortStrategy
from model.sorting.direction import SortDirection
from model.sorting.ram_strategy import RamSortStrategy
from model.sorting.storage_strategy import StorageSortStrategy


class ComputerModel(IComputerModel):
    """Encapsulates catalog state, device persistence, and data processing operations."""

    def __init__(self, initial_devices: Sequence[Interface]) -> None:
        """Initialize ComputerModel with devices and default sorting strategies.

        Args:
            initial_devices: Sequence of computer entities.
        """
        self._initial_devices: List[Interface] = list(initial_devices)
        self._current_devices: List[Interface] = list(initial_devices)
        self._active_strategy: Optional[ISortStrategy] = None
        self._current_direction: Optional[SortDirection] = None

        # Standard strategy registry (Open/Closed design: can be extended)
        self._strategies: Dict[str, ISortStrategy] = {
            "cpu": CpuSortStrategy(),
            "ram": RamSortStrategy(),
            "storage": StorageSortStrategy(),
        }

    def get_devices(self) -> Sequence[Interface]:
        """Return the sequence of current computer entities (immutable copy)."""
        return tuple(self._current_devices)

    def get_device_count(self) -> int:
        """Return total count of managed devices."""
        return len(self._current_devices)

    def get_active_strategy(self) -> Optional[ISortStrategy]:
        """Return currently applied sorting strategy."""
        return self._active_strategy

    def get_current_direction(self) -> Optional[SortDirection]:
        """Return current sorting direction enum."""
        return self._current_direction

    def get_available_strategies(self) -> Dict[str, ISortStrategy]:
        """Return mapping of available sort strategies."""
        return dict(self._strategies)

    def get_status_description(self) -> str:
        """Return formatted status text representing current catalog state."""
        if self._active_strategy is None or self._current_direction is None:
            return "Исходный порядок"
        return (
            f"Сортировка: {self._active_strategy.display_name} "
            f"({self._current_direction.label}) {self._current_direction.arrow}"
        )

    def sort_by_strategy_key(self, key_name: str) -> Tuple[Sequence[Interface], str]:
        """Apply sorting for the strategy identified by key_name.

        Toggles direction if repeated on same column; defaults to DESCENDING on first click.

        Args:
            key_name: Parameter key identifying the sort strategy.

        Returns:
            Tuple of sorted device sequence and updated status text.

        Raises:
            ModelError: If strategy key is not registered or sorting fails.
        """
        strategy = self._strategies.get(key_name)
        if strategy is None:
            raise ModelError(f"Sort strategy key '{key_name}' is not recognized.")

        try:
            if self._active_strategy is None or self._active_strategy.key_name != strategy.key_name:
                self._active_strategy = strategy
                self._current_direction = SortDirection.DESCENDING
            else:
                self._current_direction = self._current_direction.toggle()

            self._current_devices = strategy.sort(self._current_devices, self._current_direction)
            return self.get_devices(), self.get_status_description()
        except SortStrategyError as err:
            raise ModelError(f"Model sorting execution failed: {err}") from err

    def reset(self) -> None:
        """Reset devices back to original initial dataset ordering."""
        self._current_devices = list(self._initial_devices)
        self._active_strategy = None
        self._current_direction = None

    def add_device(self, device: Interface) -> None:
        """Append a device and keep the current catalog state consistent."""
        if not isinstance(device, Interface):
            raise ModelError("Only Interface-compatible devices can be added.")
        self._current_devices.append(device)
        self._initial_devices.append(device)
        self._apply_active_sort()

    def update_device(self, index: int, device: Interface) -> None:
        """Replace a catalog item at a valid zero-based index."""
        self._validate_index(index)
        if not isinstance(device, Interface):
            raise ModelError("Only Interface-compatible devices can be stored.")
        previous = self._current_devices[index]
        self._current_devices[index] = device
        initial_index = self._initial_devices.index(previous)
        self._initial_devices[initial_index] = device
        self._apply_active_sort()

    def delete_device(self, index: int) -> None:
        """Delete a catalog item and its corresponding reset entry."""
        self._validate_index(index)
        removed = self._current_devices.pop(index)
        self._initial_devices.remove(removed)
        self._apply_active_sort()

    def get_device(self, index: int) -> Interface:
        """Return a device at a valid zero-based index."""
        self._validate_index(index)
        return self._current_devices[index]

    def _validate_index(self, index: int) -> None:
        """Reject indexes that do not address a current device."""
        if not isinstance(index, int) or not 0 <= index < len(self._current_devices):
            raise ModelError(f"Device index '{index}' is out of range.")

    def _apply_active_sort(self) -> None:
        """Reapply the selected strategy after a collection mutation."""
        if self._active_strategy is not None and self._current_direction is not None:
            self._current_devices = self._active_strategy.sort(
                self._current_devices,
                self._current_direction,
            )

    def __repr__(self) -> str:
        """Return developer representation."""
        return (
            f"{self.__class__.__name__}("
            f"devices_count={len(self._current_devices)}, "
            f"active_strategy={self._active_strategy!r}, "
            f"direction={self._current_direction!r})"
        )

    def __str__(self) -> str:
        """Return human-readable representation."""
        return f"ComputerModel(Total: {len(self._current_devices)}, State: {self.get_status_description()})"

"""Laptop computer domain entity with autonomous battery duration specification."""

from __future__ import annotations

from model.computer import Computer
from model.exceptions import EntityValidationError


class Laptop(Computer):
    """Portable computer entity characterized by battery duration in hours."""

    def __init__(
        self,
        cpu: str = "Intel Core i7",
        ram: int = 16,
        storage: int = 512,
        battery_life: int = 8,
    ) -> None:
        """Initialize Laptop instance.

        Args:
            cpu: CPU model name.
            ram: RAM capacity in GB.
            storage: Storage capacity in GB.
            battery_life: Autonomous operation duration in hours.
        """
        super().__init__(cpu=cpu, ram=ram, storage=storage)
        self.battery_life = battery_life

    @property
    def battery_life(self) -> int:
        """Return battery autonomy in hours."""
        value = self.get_parameter("battery_life")
        return int(value) if value is not None else 0

    @battery_life.setter
    def battery_life(self, value: int) -> None:
        """Set battery duration with validation."""
        if not isinstance(value, int) or value <= 0:
            raise EntityValidationError(f"Battery life must be a positive integer, got: {value}")
        self.set_parameter("battery_life", value)

    def __repr__(self) -> str:
        """Return unambiguous developer representation."""
        return (
            f"{self.__class__.__name__}("
            f"cpu={self.cpu!r}, "
            f"ram={self.ram!r}, "
            f"storage={self.storage!r}, "
            f"battery_life={self.battery_life!r})"
        )

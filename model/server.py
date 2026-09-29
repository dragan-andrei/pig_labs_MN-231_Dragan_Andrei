"""Server computer domain entity with rack unit (U) standard form specification."""

from __future__ import annotations

from model.computer import Computer
from model.exceptions import EntityValidationError


class Server(Computer):
    """Rack-mounted server entity characterized by chassis rack unit height."""

    def __init__(
        self,
        cpu: str = "AMD EPYC",
        ram: int = 64,
        storage: int = 2000,
        rack_units: int = 2,
    ) -> None:
        """Initialize Server instance.

        Args:
            cpu: CPU model name.
            ram: RAM capacity in GB.
            storage: Storage capacity in GB.
            rack_units: Height standard in rack units (U).
        """
        super().__init__(cpu=cpu, ram=ram, storage=storage)
        self.rack_units = rack_units

    @property
    def rack_units(self) -> int:
        """Return height in rack units (U)."""
        value = self.get_parameter("rack_units")
        return int(value) if value is not None else 0

    @rack_units.setter
    def rack_units(self, value: int) -> None:
        """Set rack unit height with validation."""
        if not isinstance(value, int) or value <= 0:
            raise EntityValidationError(f"Rack units must be a positive integer, got: {value}")
        self.set_parameter("rack_units", value)

    def __repr__(self) -> str:
        """Return unambiguous developer representation."""
        return (
            f"{self.__class__.__name__}("
            f"cpu={self.cpu!r}, "
            f"ram={self.ram!r}, "
            f"storage={self.storage!r}, "
            f"rack_units={self.rack_units!r})"
        )

"""Personal Computer (PC) domain entity with chassis form factor specification."""

from __future__ import annotations

from model.computer import Computer
from model.exceptions import EntityValidationError


class PC(Computer):
    """Desktop computer entity characterized by chassis form-factor."""

    def __init__(
        self,
        cpu: str = "Intel Core i5",
        ram: int = 16,
        storage: int = 512,
        form_factor: str = "ATX",
    ) -> None:
        """Initialize PC instance.

        Args:
            cpu: CPU model name.
            ram: RAM capacity in GB.
            storage: Storage capacity in GB.
            form_factor: Chassis standard (e.g. 'ATX', 'Mini-ITX').
        """
        super().__init__(cpu=cpu, ram=ram, storage=storage)
        self.form_factor = form_factor

    @property
    def form_factor(self) -> str:
        """Return chassis form factor specification."""
        value = self.get_parameter("form_factor")
        return str(value) if value is not None else ""

    @form_factor.setter
    def form_factor(self, value: str) -> None:
        """Set chassis form factor with validation."""
        if not isinstance(value, str) or not value.strip():
            raise EntityValidationError("Form factor must be a non-empty string.")
        self.set_parameter("form_factor", value.strip())

    def __repr__(self) -> str:
        """Return unambiguous developer representation."""
        return (
            f"{self.__class__.__name__}("
            f"cpu={self.cpu!r}, "
            f"ram={self.ram!r}, "
            f"storage={self.storage!r}, "
            f"form_factor={self.form_factor!r})"
        )

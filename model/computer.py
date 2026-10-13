"""Base computer entity implementing core system specifications."""

from __future__ import annotations

from typing import Any, Dict, Optional

from model.exceptions import EntityValidationError
from model.interface import Interface


class Computer(Interface):
    """Base computer domain entity holding CPU, RAM, and storage specifications."""

    def __init__(self, cpu: str = "Unknown CPU", ram: int = 8, storage: int = 256) -> None:
        """Initialize computer instance with core parameters.

        Args:
            cpu: Central Processing Unit identifier/model.
            ram: Random Access Memory capacity in gigabytes (GB).
            storage: Storage capacity in gigabytes (GB).

        Raises:
            EntityValidationError: If initialization values fail validation.
        """
        self._parameters: Dict[str, Any] = {}
        self.cpu = cpu
        self.ram = ram
        self.storage = storage

    def set_parameter(self, param_name: str, value: Any) -> None:
        """Assign value to a specified parameter.

        Args:
            param_name: The identifier of the parameter.
            value: The value to be set.

        Raises:
            EntityValidationError: If param_name is empty or invalid.
        """
        if not isinstance(param_name, str) or not param_name.strip():
            raise EntityValidationError("Parameter name must be a non-empty string.")
        self._parameters[param_name] = value

    def get_parameter(self, param_name: str) -> Optional[Any]:
        """Retrieve the value of a specified parameter.

        Args:
            param_name: The identifier of the parameter.

        Returns:
            The parameter value, or None if not set.
        """
        return self._parameters.get(param_name, None)

    def get_parameters(self) -> Dict[str, Any]:
        """Return a defensive copy of the device parameters."""
        return dict(self._parameters)

    @property
    def cpu(self) -> str:
        """Return CPU model specification."""
        value = self.get_parameter("cpu")
        return str(value) if value is not None else ""

    @cpu.setter
    def cpu(self, value: str) -> None:
        """Set CPU model specification with validation."""
        if not isinstance(value, str) or not value.strip():
            raise EntityValidationError("CPU must be a non-empty string.")
        self.set_parameter("cpu", value.strip())

    @property
    def ram(self) -> int:
        """Return RAM capacity in gigabytes."""
        value = self.get_parameter("ram")
        return int(value) if value is not None else 0

    @ram.setter
    def ram(self, value: int) -> None:
        """Set RAM capacity with validation."""
        if not isinstance(value, int) or value <= 0:
            raise EntityValidationError(f"RAM must be a positive integer, got: {value}")
        self.set_parameter("ram", value)

    @property
    def storage(self) -> int:
        """Return storage capacity in gigabytes."""
        value = self.get_parameter("storage")
        return int(value) if value is not None else 0

    @storage.setter
    def storage(self, value: int) -> None:
        """Set storage capacity with validation."""
        if not isinstance(value, int) or value <= 0:
            raise EntityValidationError(f"Storage must be a positive integer, got: {value}")
        self.set_parameter("storage", value)

    def __str__(self) -> str:
        """Return human-readable string representation."""
        params_str = ", ".join(f"{k}={v}" for k, v in sorted(self._parameters.items()))
        return f"{self.__class__.__name__}({params_str})"

    def __repr__(self) -> str:
        """Return unambiguous developer representation."""
        return (
            f"{self.__class__.__name__}("
            f"cpu={self.cpu!r}, "
            f"ram={self.ram!r}, "
            f"storage={self.storage!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality based on stored specifications."""
        if not isinstance(other, self.__class__):
            return False
        return self._parameters == other._parameters

    def __hash__(self) -> int:
        """Generate hash based on class and immutable parameter tuple."""
        items = tuple(sorted((k, str(v)) for k, v in self._parameters.items()))
        return hash((self.__class__.__name__, items))

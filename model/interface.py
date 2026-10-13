"""Abstract interface contract for computer domain entities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class Interface(ABC):
    """Abstract contract for objects that store and provide computer parameters."""

    @abstractmethod
    def set_parameter(self, param_name: str, value: Any) -> None:
        """Assign value to a specified parameter.

        Args:
            param_name: The identifier of the parameter.
            value: The value to be set.

        Raises:
            EntityValidationError: If parameter name or value is invalid.
        """

    @abstractmethod
    def get_parameter(self, param_name: str) -> Optional[Any]:
        """Retrieve the value of a specified parameter.

        Args:
            param_name: The identifier of the parameter.

        Returns:
            The parameter value, or None if not defined.
        """

    @abstractmethod
    def get_parameters(self) -> dict[str, Any]:
        """Return a copy of all public device parameters."""

    @abstractmethod
    def __str__(self) -> str:
        """Return human-readable string representation."""

    @abstractmethod
    def __repr__(self) -> str:
        """Return unambiguous developer representation."""

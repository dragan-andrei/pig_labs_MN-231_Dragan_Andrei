"""Factory for constructing validated domain devices from form data."""

from __future__ import annotations

from typing import Any, Dict, Type

from model.exceptions import ModelError
from model.interface import Interface
from model.laptop import Laptop
from model.pc import PC
from model.server import Server


class DeviceFactory:
    """Create concrete device entities without coupling the view to the model."""

    _device_types: Dict[str, Type[Interface]] = {
        "PC": PC,
        "Laptop": Laptop,
        "Server": Server,
    }

    @classmethod
    def create(cls, device_type: str, values: Dict[str, Any]) -> Interface:
        """Create a device from normalized form values."""
        device_class = cls._device_types.get(device_type)
        if device_class is None:
            raise ModelError(f"Unknown device type: {device_type}")
        try:
            return device_class(**values)
        except (TypeError, ValueError) as error:
            raise ModelError(f"Invalid {device_type} parameters: {error}") from error

    @classmethod
    def supported_types(cls) -> tuple[str, ...]:
        """Return device types supported by the catalog form."""
        return tuple(cls._device_types)

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(types={self.supported_types()!r})"
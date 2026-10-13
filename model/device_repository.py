"""Persistence abstractions and JSON storage for catalog devices."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Sequence

from model.device_factory import DeviceFactory
from model.exceptions import ModelError
from model.interface import Interface


class IDeviceRepository(ABC):
    """Contract for loading and storing domain devices."""

    @abstractmethod
    def load(self) -> Sequence[Interface]:
        """Load devices from the configured storage."""

    @abstractmethod
    def save(self, devices: Sequence[Interface]) -> None:
        """Persist devices to the configured storage."""


class JsonDeviceRepository(IDeviceRepository):
    """Persist device type and validated parameters in a JSON file."""

    def __init__(self, file_path: Path) -> None:
        """Initialize repository with a JSON file path."""
        self._file_path = file_path

    def load(self) -> Sequence[Interface]:
        """Load devices, returning an empty sequence for a missing file."""
        if not self._file_path.exists():
            return []
        try:
            raw_devices = json.loads(self._file_path.read_text(encoding="utf-8"))
            if not isinstance(raw_devices, list):
                raise ModelError("Saved device data must be a JSON list.")
            return [self._deserialize(item) for item in raw_devices]
        except (OSError, json.JSONDecodeError, TypeError, ModelError) as error:
            raise ModelError(f"Unable to load saved devices: {error}") from error

    @property
    def has_saved_data(self) -> bool:
        """Return whether this repository already contains a catalog file."""
        return self._file_path.is_file()

    def save(self, devices: Sequence[Interface]) -> None:
        """Write devices atomically enough for normal application shutdowns."""
        records = [
            {
                "type": device.__class__.__name__,
                "parameters": device.get_parameters(),
            }
            for device in devices
        ]
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self._file_path.with_suffix(".tmp")
        try:
            temporary_path.write_text(
                json.dumps(records, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            temporary_path.replace(self._file_path)
        except OSError as error:
            raise ModelError(f"Unable to save devices: {error}") from error

    def _deserialize(self, record: Any) -> Interface:
        """Convert one JSON record back to a validated domain object."""
        if not isinstance(record, dict):
            raise ModelError("Each saved device must be a JSON object.")
        device_type = record.get("type")
        parameters = record.get("parameters")
        if not isinstance(device_type, str) or not isinstance(parameters, dict):
            raise ModelError("Saved device records require type and parameters.")
        return DeviceFactory.create(device_type, parameters)

    def __repr__(self) -> str:
        """Return an unambiguous developer representation."""
        return f"{self.__class__.__name__}(file_path={str(self._file_path)!r})"
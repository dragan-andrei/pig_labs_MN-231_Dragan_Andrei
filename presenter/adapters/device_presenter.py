"""Device presenter adapters converting domain entities to UI presentation format."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from model.interface import Interface
from view.theme import PurpleTheme
from view.view_model import DeviceViewModel


class IDevicePresenter(ABC):
    """Abstract contract for formatting a domain computer entity for UI presentation."""

    @property
    @abstractmethod
    def type_badge(self) -> Tuple[str, str, str]:
        """Return tuple of (badge_label, background_color, text_color)."""

    @property
    @abstractmethod
    def cpu_text(self) -> str:
        """Return formatted processor string."""

    @property
    @abstractmethod
    def ram_text(self) -> str:
        """Return formatted RAM string."""

    @property
    @abstractmethod
    def storage_text(self) -> str:
        """Return formatted Storage string."""

    @property
    @abstractmethod
    def extra_text(self) -> str:
        """Return formatted device-specific detail string."""

    @abstractmethod
    def to_view_model(self) -> DeviceViewModel:
        """Convert presentation attributes to a standardized DeviceViewModel."""


class BaseDevicePresenter(IDevicePresenter):
    """Base presenter adapter for generic computer devices."""

    def __init__(self, device: Interface) -> None:
        """Initialize adapter wrapping a domain device.

        Args:
            device: Domain entity implementing Interface.
        """
        self._device = device

    @property
    def type_badge(self) -> Tuple[str, str, str]:
        """Return generic device badge attributes."""
        return "DEVICE", PurpleTheme.BADGE_PC_BG, PurpleTheme.BADGE_PC_TEXT

    @property
    def cpu_text(self) -> str:
        """Return processor specification."""
        value = self._device.get_parameter("cpu")
        return str(value) if value else "N/A"

    @property
    def ram_text(self) -> str:
        """Return memory specification with GB suffix."""
        value = self._device.get_parameter("ram")
        return f"{value} GB" if value is not None else "N/A"

    @property
    def storage_text(self) -> str:
        """Return storage specification with GB suffix."""
        value = self._device.get_parameter("storage")
        return f"{value} GB" if value is not None else "N/A"

    @property
    def extra_text(self) -> str:
        """Return fallback placeholder for extra details."""
        return "-"

    def to_view_model(self) -> DeviceViewModel:
        """Create and return a DeviceViewModel from formatted properties."""
        badge_label, badge_bg, badge_fg = self.type_badge
        return DeviceViewModel(
            type_name=badge_label,
            badge_bg=badge_bg,
            badge_fg=badge_fg,
            cpu_text=self.cpu_text,
            ram_text=self.ram_text,
            storage_text=self.storage_text,
            extra_text=self.extra_text,
        )

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(device={self._device!r})"


class PCDevicePresenter(BaseDevicePresenter):
    """Specialized presenter adapter for Desktop PC systems."""

    @property
    def type_badge(self) -> Tuple[str, str, str]:
        """Return PC-specific badge attributes."""
        return "PC", PurpleTheme.BADGE_PC_BG, PurpleTheme.BADGE_PC_TEXT

    @property
    def extra_text(self) -> str:
        """Return chassis form factor detail string."""
        value = self._device.get_parameter("form_factor")
        return str(value) if value else "-"


class LaptopDevicePresenter(BaseDevicePresenter):
    """Specialized presenter adapter for Laptop systems."""

    @property
    def type_badge(self) -> Tuple[str, str, str]:
        """Return Laptop-specific badge attributes."""
        return "Laptop", PurpleTheme.BADGE_LAPTOP_BG, PurpleTheme.BADGE_LAPTOP_TEXT

    @property
    def extra_text(self) -> str:
        """Return battery autonomy detail string."""
        value = self._device.get_parameter("battery_life")
        return f"{value} hrs" if value is not None else "-"


class ServerDevicePresenter(BaseDevicePresenter):
    """Specialized presenter adapter for Server systems."""

    @property
    def type_badge(self) -> Tuple[str, str, str]:
        """Return Server-specific badge attributes."""
        return "Server", PurpleTheme.BADGE_SERVER_BG, PurpleTheme.BADGE_SERVER_TEXT

    @property
    def extra_text(self) -> str:
        """Return rack unit specification detail string."""
        value = self._device.get_parameter("rack_units")
        return f"{value}U Rack" if value is not None else "-"

"""Factory for creating device presenter adapters based on entity type."""

from __future__ import annotations

from model.interface import Interface
from model.laptop import Laptop
from model.pc import PC
from model.server import Server
from presenter.adapters.device_presenter import (
    BaseDevicePresenter,
    IDevicePresenter,
    LaptopDevicePresenter,
    PCDevicePresenter,
    ServerDevicePresenter,
)


class DevicePresenterFactory:
    """Factory responsible for instantiating polymorphic device presenters."""

    @staticmethod
    def create(device: Interface) -> IDevicePresenter:
        """Create and return a concrete presenter adapter matching the device type.

        Args:
            device: Domain entity implementing Interface.

        Returns:
            An IDevicePresenter instance tailored for the specific device class.
        """
        if isinstance(device, Laptop):
            return LaptopDevicePresenter(device)
        if isinstance(device, Server):
            return ServerDevicePresenter(device)
        if isinstance(device, PC):
            return PCDevicePresenter(device)
        return BaseDevicePresenter(device)

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}()"

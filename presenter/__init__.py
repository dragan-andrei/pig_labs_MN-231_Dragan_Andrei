"""Presenter package connecting domain models to user interface views."""

from __future__ import annotations

from presenter.adapters import (
    BaseDevicePresenter,
    DevicePresenterFactory,
    IDevicePresenter,
    LaptopDevicePresenter,
    PCDevicePresenter,
    ServerDevicePresenter,
)
from presenter.chart_presenter import ChartPresenter
from presenter.chart_presenter_interface import IChartPresenter
from presenter.computer_presenter import ComputerPresenter
from presenter.presenter_interface import IComputerPresenter

__all__ = [
    "IChartPresenter",
    "ChartPresenter",
    "IComputerPresenter",
    "ComputerPresenter",
    "IDevicePresenter",
    "BaseDevicePresenter",
    "PCDevicePresenter",
    "LaptopDevicePresenter",
    "ServerDevicePresenter",
    "DevicePresenterFactory",
]

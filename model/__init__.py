"""Model package encapsulating entities, catalog generation, and data processing."""

from __future__ import annotations

from model.catalog import ComputerCatalog
from model.computer import Computer
from model.computer_model import ComputerModel
from model.exceptions import (
    DomainError,
    EntityValidationError,
    ModelError,
    SortStrategyError,
)
from model.interface import Interface
from model.laptop import Laptop
from model.model_interface import IComputerModel
from model.pc import PC
from model.server import Server
from model.sorting import (
    CpuPowerCatalog,
    CpuSortStrategy,
    ISortStrategy,
    RamSortStrategy,
    SortDirection,
    StorageSortStrategy,
)

__all__ = [
    "Interface",
    "Computer",
    "PC",
    "Laptop",
    "Server",
    "ComputerCatalog",
    "IComputerModel",
    "ComputerModel",
    "DomainError",
    "EntityValidationError",
    "ModelError",
    "SortStrategyError",
    "ISortStrategy",
    "SortDirection",
    "CpuPowerCatalog",
    "CpuSortStrategy",
    "RamSortStrategy",
    "StorageSortStrategy",
]

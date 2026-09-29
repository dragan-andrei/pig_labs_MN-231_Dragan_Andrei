"""Catalog factory responsible for generating standard laboratory computer collections."""

from __future__ import annotations

from typing import List

from model.interface import Interface
from model.laptop import Laptop
from model.pc import PC
from model.server import Server


class ComputerCatalog:
    """Factory creating initial collections of PC, Laptop, and Server devices."""

    def create_devices(self) -> List[Interface]:
        """Generate and return 30 diverse computer systems for the catalog.

        Returns:
            List containing 10 PCs, 10 Laptops, and 10 Servers with configured specs.
        """
        devices: List[Interface] = []

        # 1. Generate 10 Personal Computers
        pc_cpus = (
            "Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9", "AMD Ryzen 3",
            "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9", "Intel Core i5-13400", "AMD Ryzen 5 5600X",
        )
        for index, cpu in enumerate(pc_cpus):
            devices.append(
                PC(
                    cpu=cpu,
                    ram=8 + (index % 4) * 8,
                    storage=256 + index * 256,
                    form_factor="Mini-ITX" if index % 2 == 0 else "ATX",
                )
            )

        # 2. Generate 10 Laptop Systems
        laptop_cpus = (
            "Apple M1", "Apple M2", "Apple M3", "Intel Core i5-1240P", "Intel Core i7-12700H",
            "AMD Ryzen 7 6800U", "Intel Core Ultra 7", "AMD Ryzen 9 7940HS", "Apple M2 Pro", "Apple M3 Max",
        )
        for index, cpu in enumerate(laptop_cpus):
            devices.append(
                Laptop(
                    cpu=cpu,
                    ram=8 + (index % 3) * 8,
                    storage=512 + (index % 4) * 512,
                    battery_life=6 + index,
                )
            )

        # 3. Generate 10 Enterprise Servers
        server_cpus = (
            "AMD EPYC 7763", "AMD EPYC 9654", "Intel Xeon Silver 4314", "Intel Xeon Gold 6330", "Intel Xeon Platinum 8380",
            "AMD EPYC 7543", "Intel Xeon E-2388G", "AMD EPYC 9354", "Intel Xeon Gold 5418Y", "AMD EPYC 7713",
        )
        for index, cpu in enumerate(server_cpus):
            devices.append(
                Server(
                    cpu=cpu,
                    ram=32 + index * 32,
                    storage=1000 + index * 2000,
                    rack_units=1 + index % 4,
                )
            )

        return devices

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}()"

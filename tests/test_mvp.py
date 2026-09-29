"""Comprehensive test suite verifying Model-View-Presenter architecture compliance."""

from __future__ import annotations

import unittest
from typing import List, Optional, Sequence

from model.catalog import ComputerCatalog
from model.computer import Computer
from model.computer_model import ComputerModel
from model.exceptions import EntityValidationError, ModelError
from model.interface import Interface
from model.laptop import Laptop
from model.pc import PC
from model.server import Server
from model.sorting.direction import SortDirection
from presenter.adapters.presenter_factory import DevicePresenterFactory
from presenter.computer_presenter import ComputerPresenter
from presenter.presenter_interface import IComputerPresenter
from view.view_interface import IComputerView
from view.view_model import DeviceViewModel


class MockComputerView(IComputerView):
    """Mock implementation of IComputerView to test Presenter behavior in isolation."""

    def __init__(self) -> None:
        self.presenter: Optional[IComputerPresenter] = None
        self.displayed_devices: Sequence[DeviceViewModel] = []
        self.last_status_description: str = ""
        self.last_total_count: int = 0
        self.last_active_key: Optional[str] = None
        self.last_direction_arrow: Optional[str] = None
        self.last_error: Optional[str] = None

    def set_presenter(self, presenter: IComputerPresenter) -> None:
        self.presenter = presenter

    def display_devices(
        self,
        devices: Sequence[DeviceViewModel],
        status_description: str,
        total_count: int,
    ) -> None:
        self.displayed_devices = devices
        self.last_status_description = status_description
        self.last_total_count = total_count

    def update_sort_button_state(
        self,
        active_key: Optional[str],
        direction_arrow: Optional[str],
    ) -> None:
        self.last_active_key = active_key
        self.last_direction_arrow = direction_arrow

    def show_error(self, message: str) -> None:
        self.last_error = message

    def start(self) -> None:
        pass

    def close(self) -> None:
        pass


class TestDomainEntities(unittest.TestCase):
    """Test domain models in model/."""

    def test_pc_creation_and_validation(self) -> None:
        pc = PC(cpu="Intel Core i7", ram=32, storage=1024, form_factor="ATX")
        self.assertEqual(pc.cpu, "Intel Core i7")
        self.assertEqual(pc.ram, 32)
        self.assertEqual(pc.storage, 1024)
        self.assertEqual(pc.form_factor, "ATX")

        with self.assertRaises(EntityValidationError):
            pc.ram = -5

        with self.assertRaises(EntityValidationError):
            pc.cpu = ""

    def test_laptop_creation_and_validation(self) -> None:
        laptop = Laptop(cpu="Apple M3", ram=16, storage=512, battery_life=14)
        self.assertEqual(laptop.battery_life, 14)

        with self.assertRaises(EntityValidationError):
            laptop.battery_life = 0

    def test_server_creation_and_validation(self) -> None:
        server = Server(cpu="AMD EPYC", ram=128, storage=4000, rack_units=4)
        self.assertEqual(server.rack_units, 4)

        with self.assertRaises(EntityValidationError):
            server.rack_units = -1


class TestCatalogAndModel(unittest.TestCase):
    """Test ComputerCatalog and ComputerModel."""

    def setUp(self) -> None:
        self.catalog = ComputerCatalog()
        self.devices = self.catalog.create_devices()
        self.model = ComputerModel(self.devices)

    def test_catalog_device_count(self) -> None:
        self.assertEqual(len(self.devices), 30)
        self.assertEqual(self.model.get_device_count(), 30)

    def test_model_sorting_toggle(self) -> None:
        # First sort: RAM descending
        items, status = self.model.sort_by_strategy_key("ram")
        self.assertEqual(self.model.get_current_direction(), SortDirection.DESCENDING)
        self.assertTrue(items[0].ram >= items[-1].ram)
        self.assertIn("от большего к меньшему", status)

        # Second sort on same key: RAM ascending
        items2, status2 = self.model.sort_by_strategy_key("ram")
        self.assertEqual(self.model.get_current_direction(), SortDirection.ASCENDING)
        self.assertTrue(items2[0].ram <= items2[-1].ram)
        self.assertIn("от меньшего к большему", status2)

        # Third sort on different key: Storage descending
        items3, status3 = self.model.sort_by_strategy_key("storage")
        self.assertEqual(self.model.get_current_direction(), SortDirection.DESCENDING)
        self.assertTrue(items3[0].storage >= items3[-1].storage)

    def test_unknown_sort_key_raises_error(self) -> None:
        with self.assertRaises(ModelError):
            self.model.sort_by_strategy_key("invalid_key")


class TestPresenterArchitecture(unittest.TestCase):
    """Test presenter mediation between model and view."""

    def setUp(self) -> None:
        self.catalog = ComputerCatalog()
        self.model = ComputerModel(self.catalog.create_devices())
        self.view = MockComputerView()
        self.presenter = ComputerPresenter(model=self.model, view=self.view)
        self.view.set_presenter(self.presenter)

    def test_initialization(self) -> None:
        self.presenter.initialize()
        self.assertEqual(self.view.last_total_count, 30)
        self.assertEqual(len(self.view.displayed_devices), 30)
        self.assertEqual(self.view.last_status_description, "Исходный порядок")
        self.assertIsNone(self.view.last_active_key)

    def test_handle_sort_requested_delegates_to_model_and_updates_view(self) -> None:
        self.presenter.initialize()
        self.presenter.handle_sort_requested("cpu")

        self.assertEqual(self.view.last_active_key, "cpu")
        self.assertEqual(self.view.last_direction_arrow, "▼")
        self.assertIn("CPU Power", self.view.last_status_description)
        self.assertEqual(len(self.view.displayed_devices), 30)

        # Second sort: toggle direction to ascending
        self.presenter.handle_sort_requested("cpu")
        self.assertEqual(self.view.last_direction_arrow, "▲")

    def test_polymorphic_presenter_adapters(self) -> None:
        pc = PC(form_factor="Mini-ITX")
        laptop = Laptop(battery_life=10)
        server = Server(rack_units=3)

        pc_pres = DevicePresenterFactory.create(pc)
        lap_pres = DevicePresenterFactory.create(laptop)
        srv_pres = DevicePresenterFactory.create(server)

        self.assertEqual(pc_pres.type_badge[0], "PC")
        self.assertEqual(pc_pres.extra_text, "Mini-ITX")

        self.assertEqual(lap_pres.type_badge[0], "Laptop")
        self.assertEqual(lap_pres.extra_text, "10 hrs")

        self.assertEqual(srv_pres.type_badge[0], "Server")
        self.assertEqual(srv_pres.extra_text, "3U Rack")


if __name__ == "__main__":
    unittest.main()

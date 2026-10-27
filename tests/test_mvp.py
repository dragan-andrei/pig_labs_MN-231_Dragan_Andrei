"""Comprehensive test suite verifying Model-View-Presenter architecture compliance."""

from __future__ import annotations

import unittest
from typing import Dict, List, Optional, Sequence

from model.catalog import ComputerCatalog
from model.computer import Computer
from model.computer_model import ComputerModel
from model.exceptions import ChartDataError, EntityValidationError, ModelError
from model.interface import Interface
from model.laptop import Laptop
from model.pc import PC
from model.server import Server
from model.sorting.direction import SortDirection
from presenter.adapters.presenter_factory import DevicePresenterFactory
from presenter.computer_presenter import ComputerPresenter
from presenter.presenter_interface import IComputerPresenter
from view.chart_view_interface import IChartView
from view.chart_view_model import ChartViewModel
from view.view_interface import IComputerView
from view.view_model import DeviceViewModel


class MockChartView(IChartView):
    """Mock chart frame recording presenter output."""

    def __init__(self) -> None:
        self.presenter: Optional[object] = None
        self.options: Dict[str, str] = {}
        self.active_key: str = ""
        self.chart: Optional[ChartViewModel] = None
        self.arrow: Optional[str] = None
        self.error: Optional[str] = None
        self.opened: bool = True

    def set_presenter(self, presenter: object) -> None:
        self.presenter = presenter

    def set_metric_options(self, options: Dict[str, str], active_key: str) -> None:
        self.options, self.active_key = dict(options), active_key

    def render_chart(self, chart: ChartViewModel) -> None:
        self.chart = chart

    def update_sort_state(self, arrow: Optional[str]) -> None:
        self.arrow = arrow

    def show_error(self, message: str) -> None:
        self.error = message

    def is_open(self) -> bool:
        return self.opened

    def focus(self) -> None:
        pass

    def close(self) -> None:
        self.opened = False


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

    def open_chart_view(self) -> IChartView:
        self.chart_view = MockChartView()
        return self.chart_view

    def focus_chart_view(self) -> None:
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


class TestChartIntegration(unittest.TestCase):
    """Verify chart data flow Model -> ChartPresenter -> IChartView."""

    def setUp(self) -> None:
        self.model = ComputerModel(ComputerCatalog().create_devices())
        self.view = MockComputerView()
        self.presenter = ComputerPresenter(model=self.model, view=self.view)
        self.view.set_presenter(self.presenter)
        self.presenter.initialize()

    def test_model_builds_series(self) -> None:
        series = self.model.get_chart_series("ram", SortDirection.DESCENDING)
        self.assertEqual(len(series), 30)
        self.assertEqual(list(series.values), sorted(series.values, reverse=True))

    def test_unknown_metric_raises(self) -> None:
        with self.assertRaises(ChartDataError):
            self.model.get_chart_series("gpu")

    def test_chart_requested_renders_and_sorts(self) -> None:
        self.presenter.handle_chart_requested()
        chart_view = self.view.chart_view
        self.assertIn("cpu", chart_view.options)
        self.assertIsNotNone(chart_view.chart)
        self.assertEqual(len(chart_view.chart.values), 30)

        chart_view.presenter.handle_sort_requested()
        self.assertEqual(chart_view.arrow, SortDirection.DESCENDING.arrow)
        values = list(chart_view.chart.values)
        self.assertEqual(values, sorted(values, reverse=True))

        chart_view.presenter.handle_metric_selected("storage")
        self.assertIn("Storage", chart_view.chart.title)

    def test_chart_refreshes_on_catalog_change(self) -> None:
        self.presenter.handle_chart_requested()
        self.presenter.handle_delete_requested(0)
        self.assertEqual(len(self.view.chart_view.chart.values), 29)


if __name__ == "__main__":
    unittest.main()

"""Tests for catalog persistence across model instances."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from model.computer_model import ComputerModel
from model.device_repository import JsonDeviceRepository
from model.laptop import Laptop
from model.pc import PC


class TestDevicePersistence(unittest.TestCase):
    """Verify that CRUD changes survive a new model instance."""

    def test_crud_changes_are_restored_from_json(self) -> None:
        """Save, reload, edit and delete devices through the repository."""
        with TemporaryDirectory() as directory:
            repository = JsonDeviceRepository(Path(directory) / "devices.json")
            model = ComputerModel([PC(cpu="Initial")], repository)
            model.update_device(
                0,
                Laptop(cpu="Apple M3", ram=16, storage=512, battery_life=12),
            )
            model.add_device(PC(cpu="Intel Core i9"))

            restored = ComputerModel(repository.load(), repository)
            self.assertEqual(restored.get_device_count(), 2)
            self.assertEqual(restored.get_device(0).cpu, "Apple M3")

            restored.delete_device(1)
            restored_again = ComputerModel(repository.load(), repository)
            self.assertEqual(restored_again.get_device_count(), 1)

    def test_empty_catalog_is_preserved(self) -> None:
        """Ensure deleting the final device does not restore defaults later."""
        with TemporaryDirectory() as directory:
            repository = JsonDeviceRepository(Path(directory) / "devices.json")
            model = ComputerModel([PC()], repository)
            model.delete_device(0)

            restored = ComputerModel(repository.load(), repository)
            self.assertEqual(restored.get_device_count(), 0)


if __name__ == "__main__":
    unittest.main()

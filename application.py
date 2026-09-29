"""Application composition root configuring and launching MVP components."""

from __future__ import annotations

from model.catalog import ComputerCatalog
from model.computer_model import ComputerModel
from presenter.computer_presenter import ComputerPresenter
from view.computer_view import ComputerView


class LaboratoryApplication:
    """Composition root responsible for wiring Model, View, and Presenter components."""

    def __init__(self) -> None:
        """Instantiate and wire up catalog model, visual view, and mediating presenter."""
        # 1. Model: Domain entity storage and sorting logic
        catalog = ComputerCatalog()
        self._model = ComputerModel(initial_devices=catalog.create_devices())

        # 2. View: Pure graphical user interface
        self._view = ComputerView()

        # 3. Presenter: Coordinating mediator connecting Model and View
        self._presenter = ComputerPresenter(model=self._model, view=self._view)

        # Wire view callbacks to presenter
        self._view.set_presenter(self._presenter)

    def run(self) -> None:
        """Bootstrap initial state and execute the application main loop."""
        self._presenter.initialize()
        self._view.start()

    def __repr__(self) -> str:
        """Return developer representation."""
        return (
            f"{self.__class__.__name__}("
            f"model={self._model!r}, "
            f"view={self._view!r}, "
            f"presenter={self._presenter!r})"
        )

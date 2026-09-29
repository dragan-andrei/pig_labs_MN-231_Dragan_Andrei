"""Application entry point executing Laboratory 3 MVP architecture."""

from __future__ import annotations

from application import LaboratoryApplication


class MainBootstrap:
    """Class-based execution bootstrap for the MVP laboratory application."""

    @classmethod
    def main(cls) -> None:
        """Instantiate and execute the composition root."""
        app = LaboratoryApplication()
        app.run()


if __name__ == "__main__":
    MainBootstrap.main()
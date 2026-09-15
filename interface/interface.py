from abc import ABC, abstractmethod


class Interface(ABC):
    """Contract for objects exposing named parameters."""

    @abstractmethod
    def set_parameter(self, param_name: str, value) -> None:
        """Set a parameter value by name."""
        pass

    @abstractmethod
    def get_parameter(self, param_name: str):
        """Get a parameter value by name."""
        pass

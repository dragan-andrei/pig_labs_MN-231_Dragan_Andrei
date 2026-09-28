from abc import ABC, abstractmethod


class Interface(ABC):
    """Контракт объектов, которые хранят параметры компьютера."""

    @abstractmethod
    def set_parameter(self, param_name: str, value) -> None:
        """Изменить значение параметра по имени."""
        pass

    @abstractmethod
    def get_parameter(self, param_name: str):
        """Получить значение параметра по имени."""
        pass

from interface.interface import Interface


class Computer(Interface):

    def __init__(self, cpu: str = "Unknown CPU", ram: int = 8, storage: int = 256):
        self._parameters = {
            "cpu": cpu,
            "ram": ram,        # in GB
            "storage": storage  # in GB
        }

    def set_parameter(self, param_name: str, value) -> None:
        """Sets parameter by name."""
        self._parameters[param_name] = value

    def get_parameter(self, param_name: str):
        """Gets parameter by name."""
        return self._parameters.get(param_name, None)

    @property
    def cpu(self) -> str:
        return self._parameters.get("cpu")

    @cpu.setter
    def cpu(self, value: str) -> None:
        self.set_parameter("cpu", value)

    @property
    def ram(self) -> int:
        return self._parameters.get("ram")

    @ram.setter
    def ram(self, value: int) -> None:
        self.set_parameter("ram", value)

    @property
    def storage(self) -> int:
        return self._parameters.get("storage")

    @storage.setter
    def storage(self, value: int) -> None:
        self.set_parameter("storage", value)

    def __str__(self) -> str:
        params = [f"{k}={v}" for k, v in self._parameters.items()]
        return f"{self.__class__.__name__}({', '.join(params)})"

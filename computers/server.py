from base_class.base_class import Computer


class Server(Computer):

    def __init__(self, cpu: str = "AMD EPYC", ram: int = 64, storage: int = 2000, rack_units: int = 2):
        super().__init__(cpu=cpu, ram=ram, storage=storage)
        self.set_parameter("rack_units", rack_units)  # U height

    @property
    def rack_units(self) -> int:
        return self.get_parameter("rack_units")

    @rack_units.setter
    def rack_units(self, value: int) -> None:
        self.set_parameter("rack_units", value)

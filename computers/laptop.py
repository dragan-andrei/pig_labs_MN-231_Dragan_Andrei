from base_class.base_class import Computer


class Laptop(Computer):
    """Ноутбук с дополнительным параметром времени работы батареи."""

    def __init__(self, cpu: str = "Intel Core i7", ram: int = 16, storage: int = 512, battery_life: int = 8):
        super().__init__(cpu=cpu, ram=ram, storage=storage)
        # Время автономной работы указывается в часах.
        self.set_parameter("battery_life", battery_life)

    @property
    def battery_life(self) -> int:
        return self.get_parameter("battery_life")

    @battery_life.setter
    def battery_life(self, value: int) -> None:
        self.set_parameter("battery_life", value)

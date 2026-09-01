from base_class.base_class import Computer


class PC(Computer):

    def __init__(self, cpu: str = "Intel Core i5", ram: int = 16, storage: int = 512, form_factor: str = "ATX"):
        super().__init__(cpu=cpu, ram=ram, storage=storage)
        self.set_parameter("form_factor", form_factor)

    @property
    def form_factor(self) -> str:
        return self.get_parameter("form_factor")

    @form_factor.setter
    def form_factor(self, value: str) -> None:
        self.set_parameter("form_factor", value)

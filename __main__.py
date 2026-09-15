from typing import Callable, Sequence

import customtkinter

from computers.laptop import Laptop
from computers.pc import PC
from computers.server import Server
from interface.interface import Interface


class ComputerApp:
    """CustomTkinter application for displaying and sorting computers."""

    def __init__(self, computers: Sequence[Interface]) -> None:
        self._computers = list(computers)
        self._window = customtkinter.CTk()
        self._text_box = customtkinter.CTkTextbox(
            self._window,
            corner_radius=8,
            border_width=1,
            border_color="#39214c",
            font=("Consolas", 14),
            activate_scrollbars=True,
        )
        self._create_layout()
        self._show_computers("Initial order")

    def _create_layout(self) -> None:
        self._window.title("Lab 2 GUI")
        self._window.geometry("760x560")
        self._window.minsize(620, 420)
        self._window.configure(fg_color="#171717")
        self._window.grid_columnconfigure(0, weight=1)
        self._window.grid_rowconfigure(0, weight=1)
        self._window.grid_rowconfigure(1, weight=0)

        self._text_box.grid(row=0, column=0, padx=18, pady=(18, 12), sticky="nsew")
        self._text_box.configure(state="disabled")

        buttons = customtkinter.CTkFrame(
            self._window,
            fg_color="#251333",
            corner_radius=8,
        )
        buttons.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="ew")
        buttons.grid_columnconfigure((0, 1, 2), weight=1)

        self._create_sort_button(buttons, "Sort by CPU", self._sort_by_cpu, 0)
        self._create_sort_button(buttons, "Sort by RAM", self._sort_by_ram, 1)
        self._create_sort_button(buttons, "Sort by Storage", self._sort_by_storage, 2)

    def _create_sort_button(
        self,
        parent: customtkinter.CTkFrame,
        text: str,
        command: Callable[[], None],
        column: int,
    ) -> None:
        button = customtkinter.CTkButton(
            parent,
            text=text,
            command=command,
            height=36,
            corner_radius=7,
            fg_color="#51386d",
            hover_color="#68488a",
        )
        button.grid(row=0, column=column, padx=10, pady=10, sticky="ew")

    def _sort_by_cpu(self) -> None:
        self._computers.sort(key=lambda computer: str(computer.get_parameter("cpu")))
        self._show_computers("Sorted by CPU")

    def _sort_by_ram(self) -> None:
        self._computers.sort(key=lambda computer: computer.get_parameter("ram"), reverse=True)
        self._show_computers("Sorted by RAM (descending)")

    def _sort_by_storage(self) -> None:
        self._computers.sort(key=lambda computer: computer.get_parameter("storage"), reverse=True)
        self._show_computers("Sorted by Storage (descending)")

    def _show_computers(self, title: str) -> None:
        rows = [title, "", f"{'Type':<10}{'CPU':<25}{'RAM':>8}{'Storage':>12}", "-" * 55]
        rows.extend(
            f"{computer.__class__.__name__:<10}"
            f"{str(computer.get_parameter('cpu')):<25}"
            f"{str(computer.get_parameter('ram')):>8}"
            f"{str(computer.get_parameter('storage')):>12}"
            for computer in self._computers
        )
        self._text_box.configure(state="normal")
        self._text_box.delete("1.0", "end")
        self._text_box.insert("1.0", "\n".join(rows))
        self._text_box.configure(state="disabled")

    def run(self) -> None:
        """Start the CustomTkinter event loop."""
        self._window.mainloop()


class ComputerCatalog:
    """Factory for the computer collection used by the laboratory GUI."""

    def create_devices(self) -> list[Interface]:
        devices: list[Interface] = []
        pc_cpus = [
            "Intel Core i3", "Intel Core i5", "Intel Core i7", "Intel Core i9", "AMD Ryzen 3",
            "AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9", "Intel Core i5-13400", "AMD Ryzen 5 5600X",
        ]
        for index in range(10):
            devices.append(PC(
                cpu=pc_cpus[index],
                ram=8 + (index % 4) * 8,
                storage=256 + index * 256,
                form_factor="Mini-ITX" if index % 2 == 0 else "ATX",
            ))

        laptop_cpus = [
            "Apple M1", "Apple M2", "Apple M3", "Intel Core i5-1240P", "Intel Core i7-12700H",
            "AMD Ryzen 7 6800U", "Intel Core Ultra 7", "AMD Ryzen 9 7940HS", "Apple M2 Pro", "Apple M3 Max",
        ]
        for index in range(10):
            devices.append(Laptop(
                cpu=laptop_cpus[index],
                ram=8 + (index % 3) * 8,
                storage=512 + (index % 4) * 512,
                battery_life=6 + index,
            ))

        server_cpus = [
            "AMD EPYC 7763", "AMD EPYC 9654", "Intel Xeon Silver 4314", "Intel Xeon Gold 6330", "Intel Xeon Platinum 8380",
            "AMD EPYC 7543", "Intel Xeon E-2388G", "AMD EPYC 9354", "Intel Xeon Gold 5418Y", "AMD EPYC 7713",
        ]
        for index in range(10):
            devices.append(Server(
                cpu=server_cpus[index],
                ram=32 + index * 32,
                storage=1000 + index * 2000,
                rack_units=1 + index % 4,
            ))
        return devices


class LaboratoryApplication:
    """Composition root for the object catalog and GUI."""

    def run(self) -> None:
        ComputerApp(ComputerCatalog().create_devices()).run()


if __name__ == "__main__":
    LaboratoryApplication().run()
"""Modal form for adding and editing catalog devices."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

import customtkinter

from view.theme import PurpleTheme
from view.view_model import DeviceViewModel


class DeviceFormDialog(customtkinter.CTkToplevel):
    """Collect common and type-specific device parameters in one modal dialog."""

    def __init__(
        self,
        parent: customtkinter.CTkBaseClass,
        device_types: tuple[str, ...],
        on_submit: Callable[[str, Dict[str, Any]], None],
        device: Optional[DeviceViewModel] = None,
    ) -> None:
        """Initialize an add or edit form."""
        super().__init__(parent)
        self._on_submit = on_submit
        self._existing_device = device
        self._entries: Dict[str, customtkinter.CTkEntry] = {}
        self._error_label: Optional[customtkinter.CTkLabel] = None
        self.title("Редактировать устройство" if device else "Добавить устройство")
        self.geometry("420x430")
        self.resizable(False, False)
        self.configure(fg_color=PurpleTheme.BG_WINDOW)
        self.grid_columnconfigure(1, weight=1)
        self._type_menu = customtkinter.CTkOptionMenu(
            self, values=list(device_types), command=self._render_type_fields
        )
        self._type_menu.set(device.type_name if device else device_types[0])
        self._type_menu.grid(row=0, column=1, padx=18, pady=(20, 10), sticky="ew")
        customtkinter.CTkLabel(self, text="Тип", text_color=PurpleTheme.TEXT_PRIMARY).grid(
            row=0, column=0, padx=18, pady=(20, 10), sticky="w"
        )
        self._fields_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self._fields_frame.grid(row=1, column=0, columnspan=2, padx=18, sticky="ew")
        self._fields_frame.grid_columnconfigure(1, weight=1)
        self._render_type_fields(self._type_menu.get())
        customtkinter.CTkButton(
            self, text="Сохранить", command=self._submit, fg_color=PurpleTheme.BTN_ACTIVE_BG
        ).grid(row=2, column=0, columnspan=2, padx=18, pady=(18, 8), sticky="ew")
        customtkinter.CTkButton(
            self, text="Отмена", command=self.destroy, fg_color=PurpleTheme.BTN_DEFAULT_BG
        ).grid(row=3, column=0, columnspan=2, padx=18, pady=(0, 18), sticky="ew")
        self.transient(parent)
        self.grab_set()

    def _render_type_fields(self, device_type: str) -> None:
        """Render fields matching the selected concrete device type."""
        for child in self._fields_frame.winfo_children():
            child.destroy()
        self._entries.clear()
        fields = [("CPU", "cpu"), ("RAM (GB)", "ram"), ("Storage (GB)", "storage")]
        fields.append({"PC": ("Form factor", "form_factor"), "Laptop": ("Battery (hours)", "battery_life"), "Server": ("Rack units", "rack_units")} [device_type])
        values = self._existing_device.parameters if self._existing_device and self._existing_device.type_name == device_type else {}
        for row, (label, key) in enumerate(fields):
            customtkinter.CTkLabel(self._fields_frame, text=label, text_color=PurpleTheme.TEXT_PRIMARY).grid(
                row=row, column=0, padx=(0, 12), pady=7, sticky="w"
            )
            entry = customtkinter.CTkEntry(self._fields_frame)
            entry.insert(0, str(values.get(key, "")))
            entry.grid(row=row, column=1, pady=7, sticky="ew")
            self._entries[key] = entry

    def _submit(self) -> None:
        """Convert entry text to constructor values and submit them."""
        try:
            values: Dict[str, Any] = {"cpu": self._entries["cpu"].get().strip()}
            for key in ("ram", "storage", "form_factor", "battery_life", "rack_units"):
                if key in self._entries:
                    value = self._entries[key].get().strip()
                    values[key] = int(value) if key in {"ram", "storage", "battery_life", "rack_units"} else value
        except ValueError:
            self._show_error("RAM, storage and extra numeric fields must be integers.")
            return
        self._on_submit(self._type_menu.get(), values)
        self.destroy()

    def _show_error(self, message: str) -> None:
        """Display validation feedback without closing the form."""
        if self._error_label is None:
            self._error_label = customtkinter.CTkLabel(self, text_color="#ff8098")
            self._error_label.grid(row=4, column=0, columnspan=2, padx=18, pady=(0, 8))
        self._error_label.configure(text=message)

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(device={self._existing_device!r})"
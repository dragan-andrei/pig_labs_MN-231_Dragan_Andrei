"""Card widget rendering one device and its edit/delete actions."""

from __future__ import annotations

from typing import Callable

import customtkinter

from view.theme import PurpleTheme
from view.view_model import DeviceViewModel
from view.services.image_repository import ImageProvider


class DeviceCard(customtkinter.CTkFrame):
    """Self-contained visual card for one catalog device."""

    def __init__(
        self,
        parent: customtkinter.CTkBaseClass,
        device: DeviceViewModel,
        on_edit: Callable[[DeviceViewModel], None],
        on_delete: Callable[[int], None],
        image_provider: ImageProvider,
        row_number: int,
    ) -> None:
        """Build a card with readable specs and action buttons."""
        super().__init__(parent, fg_color=PurpleTheme.BG_CARD_EVEN, corner_radius=8)
        self._device = device
        self._on_edit = on_edit
        self._on_delete = on_delete
        self._image_provider = image_provider
        self.grid_columnconfigure(2, weight=1)

        customtkinter.CTkLabel(
            self,
            text="",
            image=self._image_provider.get(device.type_name),
            compound="center",
        ).grid(row=0, column=0, rowspan=2, padx=(10, 8), pady=8, sticky="w")

        customtkinter.CTkLabel(
            self,
            text=f"{row_number}. {device.type_name}",
            text_color=device.badge_colors[1],
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=1, padx=8, pady=(12, 4), sticky="w")
        customtkinter.CTkLabel(
            self,
            text=device.cpu_text,
            text_color=PurpleTheme.TEXT_PRIMARY,
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).grid(row=0, column=2, padx=8, pady=(12, 4), sticky="ew")
        customtkinter.CTkLabel(
            self,
            text=f"RAM {device.ram_text}  |  Storage {device.storage_text}  |  {device.extra_text}",
            text_color=PurpleTheme.TEXT_SECONDARY,
            anchor="w",
        ).grid(row=1, column=2, padx=8, pady=(0, 12), sticky="ew")
        customtkinter.CTkButton(
            self,
            text="✎",
            width=50,
            height=50,
            font=("Segoe UI Symbol", 27),
            text_color=PurpleTheme.TEXT_PRIMARY,
            fg_color=PurpleTheme.BTN_DEFAULT_BG,
            hover_color=PurpleTheme.BTN_DEFAULT_HOVER,
            command=lambda: self._on_edit(self._device),
        ).grid(row=0, column=3, padx=(4, 10), pady=(10, 4))
        customtkinter.CTkButton(
            self,
            text="✕",
            width=50,
            height=50,
            font=("Segoe UI Symbol", 27, "bold"),
            text_color="#ff304f",
            fg_color="#8f304a",
            hover_color="#b33b59",
            command=lambda: self._on_delete(self._device.device_index),
        ).grid(row=1, column=3, padx=(4, 10), pady=(0, 10))

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(device={self._device!r})"
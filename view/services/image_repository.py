"""Device image loading and caching service."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Protocol

import customtkinter
from PIL import Image


class ImageProvider(Protocol):
    """Small abstraction used by widgets to obtain device images."""

    def get(self, device_type: str) -> customtkinter.CTkImage:
        """Return the cached image associated with a device type."""


class DeviceImageRepository:
    """Load local device photos once and reuse them across all cards.

    Args:
        assets_directory: Directory containing ``pc.jpg``, ``laptop.jpg`` and
            ``server.jpg`` files.
        image_size: Width and height used by CustomTkinter for each image.

    Raises:
        FileNotFoundError: If an image is requested but is not present.
        ValueError: If the configured image size is not positive.
    """

    def __init__(self, assets_directory: Path, image_size: tuple[int, int] = (112, 76)) -> None:
        if image_size[0] <= 0 or image_size[1] <= 0:
            raise ValueError("Image dimensions must be positive.")
        self._assets_directory = assets_directory
        self._image_size = image_size
        self._cache: Dict[str, customtkinter.CTkImage] = {}

    def get(self, device_type: str) -> customtkinter.CTkImage:
        """Return a cached image for ``device_type``.

        Args:
            device_type: Device category, such as ``PC`` or ``Server``.

        Returns:
            A CustomTkinter image suitable for a ``CTkLabel``.

        Raises:
            FileNotFoundError: If the category image is missing.
            ValueError: If the category name is empty.
        """
        normalized_type = device_type.strip().lower()
        if not normalized_type:
            raise ValueError("Device type must not be empty.")
        if normalized_type not in self._cache:
            self._cache[normalized_type] = self._load(normalized_type)
        return self._cache[normalized_type]

    def _load(self, device_type: str) -> customtkinter.CTkImage:
        """Load one image from disk and convert it to a CTkImage."""
        image_path = self._assets_directory / f"{device_type}.jpg"
        if not image_path.is_file():
            raise FileNotFoundError(f"Device image not found: {image_path}")
        with Image.open(image_path) as source_image:
            image = source_image.convert("RGB")
        return customtkinter.CTkImage(
            light_image=image,
            dark_image=image,
            size=self._image_size,
        )

    def __repr__(self) -> str:
        """Return an unambiguous developer representation."""
        return f"{self.__class__.__name__}(directory={str(self._assets_directory)!r})"

    def __str__(self) -> str:
        """Return a user-friendly description of the repository."""
        return f"Device images from {self._assets_directory}"

"""Presentation data transfer model (DTO) for device rendering."""

from __future__ import annotations

from typing import Any, Dict, Tuple


class DeviceViewModel:
    """Immutable presentation model containing pre-formatted display attributes for a device row."""

    def __init__(
        self,
        type_name: str,
        badge_bg: str,
        badge_fg: str,
        cpu_text: str,
        ram_text: str,
        storage_text: str,
        extra_text: str,
        device_index: int = -1,
        parameters: Dict[str, Any] | None = None,
    ) -> None:
        """Initialize presentation model with formatted strings and theme colors.

        Args:
            type_name: Category badge text (e.g., 'PC', 'Laptop', 'Server').
            badge_bg: Background hex color code for the badge.
            badge_fg: Text foreground hex color code for the badge.
            cpu_text: Formatted CPU specification text.
            ram_text: Formatted RAM text.
            storage_text: Formatted storage text.
            extra_text: Formatted category-specific detail text.
        """
        self._type_name = type_name
        self._badge_bg = badge_bg
        self._badge_fg = badge_fg
        self._cpu_text = cpu_text
        self._ram_text = ram_text
        self._storage_text = storage_text
        self._extra_text = extra_text
        self._device_index = device_index
        self._parameters = dict(parameters or {})

    @property
    def type_name(self) -> str:
        """Return type label string."""
        return self._type_name

    @property
    def badge_colors(self) -> Tuple[str, str]:
        """Return tuple of (badge_bg, badge_fg)."""
        return self._badge_bg, self._badge_fg

    @property
    def cpu_text(self) -> str:
        """Return formatted processor string."""
        return self._cpu_text

    @property
    def ram_text(self) -> str:
        """Return formatted memory string."""
        return self._ram_text

    @property
    def storage_text(self) -> str:
        """Return formatted storage string."""
        return self._storage_text

    @property
    def extra_text(self) -> str:
        """Return formatted supplementary details."""
        return self._extra_text

    @property
    def device_index(self) -> int:
        """Return the current catalog index used by view callbacks."""
        return self._device_index

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return editable raw device parameters."""
        return dict(self._parameters)

    def __repr__(self) -> str:
        """Return developer representation."""
        return (
            f"DeviceViewModel(type={self._type_name!r}, "
            f"cpu={self._cpu_text!r}, "
            f"ram={self._ram_text!r}, "
            f"storage={self._storage_text!r})"
        )

    def __str__(self) -> str:
        """Return human-readable representation."""
        return f"{self._type_name}: {self._cpu_text} | {self._ram_text} | {self._storage_text} | {self._extra_text}"

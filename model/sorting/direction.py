"""Enumeration and descriptors for sorting direction."""

from __future__ import annotations

from enum import Enum


class SortDirection(Enum):
    """Enumeration representing ordering direction."""

    DESCENDING = "descending"
    ASCENDING = "ascending"

    @property
    def arrow(self) -> str:
        """Return directional arrow indicator for UI representation."""
        return "▼" if self == SortDirection.DESCENDING else "▲"

    @property
    def label(self) -> str:
        """Return human-readable text label."""
        return "от большего к меньшему" if self == SortDirection.DESCENDING else "от меньшего к большему"

    def toggle(self) -> SortDirection:
        """Toggle between ascending and descending order."""
        return SortDirection.ASCENDING if self == SortDirection.DESCENDING else SortDirection.DESCENDING

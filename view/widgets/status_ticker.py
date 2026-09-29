"""Animated status ticker widget displaying cyclic system status messages."""

from __future__ import annotations

from typing import Optional, Tuple

import customtkinter

from view.theme import PurpleTheme


class StatusTicker(customtkinter.CTkLabel):
    """Animated status line widget that cycles through diagnostic messages."""

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        """Initialize ticker label with monospace styling and default message.

        Args:
            parent: Parent CustomTkinter container.
        """
        super().__init__(
            parent,
            text="// DATA STREAM :: READY",
            font=("Cascadia Mono", 10),
            text_color=PurpleTheme.TEXT_MUTED,
            anchor="w",
        )
        self._messages: Tuple[str, ...] = (
            "// DATA STREAM :: READY",
            "// SORT ENGINE :: ARMED",
            "// CATALOG LINK :: STABLE",
            "// SYSTEM PULSE :: NOMINAL",
        )
        self._message_index: int = 0
        self._animation_id: Optional[str] = None
        self._animate()

    def _animate(self) -> None:
        """Cycle the status text on a lightweight timer."""
        message = self._messages[self._message_index]
        self._message_index = (self._message_index + 1) % len(self._messages)
        self.configure(text=message)
        self._animation_id = self.after(1100, self._animate)

    def destroy(self) -> None:
        """Cancel the ticker timer before destroying the widget."""
        if self._animation_id is not None:
            self.after_cancel(self._animation_id)
            self._animation_id = None
        super().destroy()

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(active_message_index={self._message_index})"

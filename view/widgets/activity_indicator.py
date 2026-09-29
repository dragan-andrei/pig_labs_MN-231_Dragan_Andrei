"""Animated live activity indicator widget with toggle and pulse bar."""

from __future__ import annotations

from typing import Optional, Tuple

import customtkinter

from view.theme import PurpleTheme


class ActivityIndicator(customtkinter.CTkFrame):
    """Activity indicator widget demonstrating pulsating UI activity and online state toggle."""

    def __init__(self, parent: customtkinter.CTkBaseClass) -> None:
        """Initialize indicator with toggle button and progress pulse.

        Args:
            parent: Parent CustomTkinter container.
        """
        super().__init__(parent, fg_color="transparent")
        self._frames: Tuple[str, ...] = ("◐", "◓", "◑", "◒")
        self._frame_index: int = 0
        self._is_online: bool = True
        self._animation_id: Optional[str] = None

        self._toggle_button = customtkinter.CTkButton(
            self,
            text="◐ LIVE",
            command=self._toggle_status,
            font=("Consolas", 11, "bold"),
            text_color=PurpleTheme.TEXT_ACCENT,
            fg_color="transparent",
            hover_color=PurpleTheme.BG_BUTTON_BAR,
            width=82,
            height=28,
        )
        self._toggle_button.pack(padx=4, pady=4)

        self._pulse_bar = customtkinter.CTkProgressBar(
            self,
            mode="indeterminate",
            width=82,
            height=4,
            progress_color=PurpleTheme.BORDER_ACTIVE,
        )
        self._pulse_bar.pack(padx=4, pady=(0, 4))
        self._pulse_bar.start()
        self._animate()

    def _animate(self) -> None:
        """Advance the spinner animation without blocking the UI thread."""
        if not self._is_online:
            return
        frame = self._frames[self._frame_index]
        self._frame_index = (self._frame_index + 1) % len(self._frames)
        self._toggle_button.configure(text=f"{frame} LIVE")
        self._animation_id = self.after(180, self._animate)

    def _toggle_status(self) -> None:
        """Toggle indicator between interactive LIVE and OFFLINE states."""
        self._is_online = not self._is_online
        if self._is_online:
            self._toggle_button.configure(
                text="◐ LIVE",
                text_color=PurpleTheme.TEXT_ACCENT,
            )
            self._pulse_bar.start()
            self._animate()
            return

        if self._animation_id is not None:
            self.after_cancel(self._animation_id)
            self._animation_id = None
        self._pulse_bar.stop()
        self._toggle_button.configure(
            text="○ OFFLINE",
            text_color=PurpleTheme.TEXT_MUTED,
        )

    def destroy(self) -> None:
        """Cancel animation loops prior to widget destruction."""
        if self._animation_id is not None:
            self.after_cancel(self._animation_id)
            self._animation_id = None
        self._pulse_bar.stop()
        super().destroy()

    def __repr__(self) -> str:
        """Return developer representation."""
        return f"{self.__class__.__name__}(is_online={self._is_online})"

"""Color palette and visual styling design tokens for the application theme."""

from __future__ import annotations

from typing import Final


class PurpleTheme:
    """Design tokens and color palette maintaining a refined purple dark aesthetic."""

    # Background layout tokens
    BG_WINDOW: Final[str] = "#140f1c"
    BG_CARD_CONTAINER: Final[str] = "#191224"
    BG_CARD_EVEN: Final[str] = "#1e152a"
    BG_CARD_ODD: Final[str] = "#241833"
    BG_HEADER_ROW: Final[str] = "#291a3c"
    BG_BUTTON_BAR: Final[str] = "#251333"

    # Border and line accents
    BORDER_SUBTLE: Final[str] = "#36204d"
    BORDER_HEADER: Final[str] = "#4c2c6d"
    BORDER_ACTIVE: Final[str] = "#8b5cf6"

    # Interactive button states
    BTN_DEFAULT_BG: Final[str] = "#51386d"
    BTN_DEFAULT_HOVER: Final[str] = "#68488a"
    BTN_ACTIVE_BG: Final[str] = "#7b47a6"
    BTN_ACTIVE_HOVER: Final[str] = "#9156c2"

    # Typography colors
    TEXT_PRIMARY: Final[str] = "#fcf4ee"
    TEXT_SECONDARY: Final[str] = "#bca9d3"
    TEXT_MUTED: Final[str] = "#8d79a5"
    TEXT_ACCENT: Final[str] = "#d8b4fe"

    # Device type badge accents
    BADGE_PC_BG: Final[str] = "#2e1b4a"
    BADGE_PC_TEXT: Final[str] = "#c084fc"
    BADGE_LAPTOP_BG: Final[str] = "#3d1b40"
    BADGE_LAPTOP_TEXT: Final[str] = "#f472b6"
    BADGE_SERVER_BG: Final[str] = "#201f4c"
    BADGE_SERVER_TEXT: Final[str] = "#93c5fd"

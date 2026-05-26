import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class BrittleHollow(BaseBody):
    """Hollow planet that crumbles into its own black hole."""

    def __init__(self) -> None:
        super().__init__(
            name="Brittle Hollow",
            color=QColor(128, 72, 172),
            radius=20,
            orbit_radius=245,
            orbit_speed=math.tau / 185,
            start_angle=math.radians(210),
        )


class HollowsLantern(BaseBody):
    """Small volcanic moon of Brittle Hollow — not clickable."""

    def __init__(self, brittle_hollow: BrittleHollow) -> None:
        super().__init__(
            name="Hollow's Lantern",
            color=QColor(222, 92, 22),
            radius=6,
            orbit_radius=26,
            orbit_speed=math.tau / 20,
            start_angle=math.radians(45),
            parent_body=brittle_hollow,
        )
        self._clickable = False

    def set_clickable(self, value: bool) -> None:
        pass  # always non-clickable

import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class BrittleHollow(BaseBody):
    """Hollow planet that crumbles into its own black hole."""

    def __init__(self) -> None:
        super().__init__(
            name="Brittle Hollow",
            color=QColor(128, 72, 172),
            radius=16,
            orbit_radius=200,
            orbit_speed=math.tau / 180,   # period ≈ 180 s
            start_angle=math.radians(210),
        )


class HollowsLantern(BaseBody):
    """Volcanic moon of Brittle Hollow."""

    def __init__(self, brittle_hollow: BrittleHollow) -> None:
        super().__init__(
            name="Hollow's Lantern",
            color=QColor(222, 92, 22),
            radius=8,
            orbit_radius=28,
            orbit_speed=math.tau / 22,    # period ≈ 22 s
            start_angle=math.radians(45),
            parent_body=brittle_hollow,
        )

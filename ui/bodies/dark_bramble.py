import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class DarkBramble(BaseBody):
    """Mysterious outer-system bramble dimension."""

    def __init__(self) -> None:
        super().__init__(
            name="Dark Bramble",
            color=QColor(26, 72, 42),
            radius=17,
            orbit_radius=285,
            orbit_speed=math.tau / 350,   # period ≈ 350 s
            start_angle=math.radians(60),
        )

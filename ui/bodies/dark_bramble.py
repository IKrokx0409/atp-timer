import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class DarkBramble(BaseBody):
    """Mysterious outer-system bramble dimension."""

    def __init__(self) -> None:
        super().__init__(
            name="Dark Bramble",
            color=QColor(26, 72, 42),
            radius=19,
            orbit_radius=328,
            orbit_speed=math.tau / 355,
            start_angle=math.radians(60),
        )

import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class GiantsDeep(BaseBody):
    """Stormy ocean planet with cyclones."""

    def __init__(self) -> None:
        super().__init__(
            name="Giant's Deep",
            color=QColor(42, 112, 192),
            radius=18,
            orbit_radius=245,
            orbit_speed=math.tau / 250,   # period ≈ 250 s
            start_angle=math.radians(300),
        )

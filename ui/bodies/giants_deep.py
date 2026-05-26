import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class GiantsDeep(BaseBody):
    """Stormy ocean planet — the largest in the system."""

    def __init__(self) -> None:
        super().__init__(
            name="Giant's Deep",
            color=QColor(42, 112, 192),
            radius=24,
            orbit_radius=292,
            orbit_speed=math.tau / 255,
            start_angle=math.radians(300),
        )

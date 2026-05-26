import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class SunStation(BaseBody):
    """Tiny artificial probe station in close solar orbit."""

    def __init__(self) -> None:
        super().__init__(
            name="Sun Station",
            color=QColor(168, 175, 188),
            radius=5,
            orbit_radius=65,
            orbit_speed=math.tau / 38,
            start_angle=0.0,
        )

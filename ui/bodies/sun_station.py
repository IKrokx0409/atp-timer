import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class SunStation(BaseBody):
    """Artificial probe station in close solar orbit."""

    def __init__(self) -> None:
        super().__init__(
            name="Sun Station",
            color=QColor(168, 175, 188),
            radius=6,
            orbit_radius=60,
            orbit_speed=math.tau / 40,    # period ≈ 40 s
            start_angle=0.0,
        )

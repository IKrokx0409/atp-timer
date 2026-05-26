import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class TimberHearth(BaseBody):
    """Home planet of the Hearthians."""

    def __init__(self) -> None:
        super().__init__(
            name="Timber Hearth",
            color=QColor(72, 152, 68),
            radius=15,
            orbit_radius=150,
            orbit_speed=math.tau / 130,   # period ≈ 130 s
            start_angle=math.radians(120),
        )


class Attlerock(BaseBody):
    """Timber Hearth's rocky moon."""

    def __init__(self, timber_hearth: TimberHearth) -> None:
        super().__init__(
            name="Attlerock",
            color=QColor(142, 132, 118),
            radius=7,
            orbit_radius=25,
            orbit_speed=math.tau / 18,    # period ≈ 18 s
            start_angle=math.radians(90),
            parent_body=timber_hearth,
        )

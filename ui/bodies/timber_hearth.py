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
            orbit_radius=182,
            orbit_speed=math.tau / 135,
            start_angle=math.radians(120),
        )


class Attlerock(BaseBody):
    """Timber Hearth's small rocky moon — not clickable."""

    def __init__(self, timber_hearth: TimberHearth) -> None:
        super().__init__(
            name="Attlerock",
            color=QColor(138, 128, 115),
            radius=5,
            orbit_radius=24,
            orbit_speed=math.tau / 16,
            start_angle=math.radians(90),
            parent_body=timber_hearth,
        )
        self._clickable = False

    def set_clickable(self, value: bool) -> None:
        pass  # always non-clickable

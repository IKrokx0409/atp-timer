import math
from PyQt6.QtGui import QColor
from .base_body import BaseBody


class AshTwin(BaseBody):
    """Sandy binary planet — hosts the Ash Twin Towers."""

    def __init__(self) -> None:
        super().__init__(
            name="Ash Twin",
            color=QColor(200, 162, 100),
            radius=14,
            orbit_radius=100,
            orbit_speed=math.tau / 80,    # period ≈ 80 s
            start_angle=math.radians(30),
        )


class EmberTwin(BaseBody):
    """Volcanic binary partner, orbits Ash Twin."""

    def __init__(self, ash_twin: AshTwin) -> None:
        super().__init__(
            name="Ember Twin",
            color=QColor(215, 92, 42),
            radius=10,
            orbit_radius=30,
            orbit_speed=math.tau / 25,    # period ≈ 25 s (fast binary)
            start_angle=math.radians(180),
            parent_body=ash_twin,
        )

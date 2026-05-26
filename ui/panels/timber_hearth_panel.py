"""
Timber Hearth settings panel.

Allows the user to resize the main window via a slider (400 – 900 px).
The resize is live: dragging the handle updates the window in real time.
"""

from PyQt6.QtCore    import Qt
from PyQt6.QtGui     import QColor
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QSlider, QSizePolicy)

from .base_panel import BasePanel, OW_ORANGE, OW_BLUE, ow_font


class TimberHearthPanel(BasePanel):
    """Settings panel for Timber Hearth — window size control."""

    _TITLE = "Timber Hearth"
    _MIN_SIZE = 400
    _MAX_SIZE = 900
    _STEP     = 50

    def __init__(self, main_window) -> None:
        super().__init__(self._TITLE, parent=None)   # free-floating, no Qt parent
        self._main = main_window
        self._build_content()
        self.adjustSize()

    # ── content ───────────────────────────────────────────────────────

    def _build_content(self) -> None:
        current = self._main.width()

        # Section label
        self._body_layout.addWidget(self._orange_label("Window Size", size=10))

        # Slider row
        slider_row = QHBoxLayout()
        slider_row.setSpacing(8)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(self._MIN_SIZE, self._MAX_SIZE)
        self._slider.setSingleStep(self._STEP)
        self._slider.setPageStep(self._STEP)
        self._slider.setValue(current)
        self._slider.setTickPosition(QSlider.TickPosition.NoTicks)
        self._slider.setStyleSheet(self._slider_style())
        self._slider.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self._value_label = self._blue_label(f"{current} px", size=10)
        self._value_label.setFixedWidth(52)
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        slider_row.addWidget(self._slider)
        slider_row.addWidget(self._value_label)
        self._body_layout.addLayout(slider_row)

        # Range hint
        hint_row = QHBoxLayout()
        lo = QLabel(f"{self._MIN_SIZE}")
        hi = QLabel(f"{self._MAX_SIZE}")
        for lbl in (lo, hi):
            lbl.setFont(ow_font(8))
            lbl.setStyleSheet("color: #7060A0; background: transparent;")
        hint_row.addWidget(lo)
        hint_row.addStretch()
        hint_row.addWidget(hi)
        self._body_layout.addLayout(hint_row)

        self._slider.valueChanged.connect(self._on_value_changed)

    # ── slider interaction ────────────────────────────────────────────

    def _on_value_changed(self, value: int) -> None:
        # Snap to nearest step
        snapped = round(value / self._STEP) * self._STEP
        snapped = max(self._MIN_SIZE, min(self._MAX_SIZE, snapped))
        self._value_label.setText(f"{snapped} px")
        self._main.set_window_size(snapped)

    # ── stylesheet ────────────────────────────────────────────────────

    @staticmethod
    def _slider_style() -> str:
        orange = OW_ORANGE.name()
        blue   = OW_BLUE.name()
        return f"""
            QSlider::groove:horizontal {{
                height: 4px;
                background: #2A2040;
                border-radius: 2px;
            }}
            QSlider::sub-page:horizontal {{
                background: {orange};
                border-radius: 2px;
            }}
            QSlider::add-page:horizontal {{
                background: #2A2040;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {orange};
                border: 2px solid {blue};
                width: 14px;
                height: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {blue};
                border-color: {orange};
            }}
        """

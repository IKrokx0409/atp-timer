"""
BasePanel — frameless floating panel in Outer Wilds style.

Colours
  Orange  #E89030  — titles, accents, slider handle
  Blue    #4A96CC  — labels, value readouts
  BG      #0D0A1A  — near-black deep-space background (semi-transparent)
  Border  #E89030  at 55 % alpha

Panels are always-on-top, frameless, and semi-transparent.
They emit `closed` when dismissed (× button or Escape).
"""

from PyQt6.QtCore    import Qt, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui     import (QPainter, QColor, QPen, QBrush,
                              QLinearGradient, QFont, QFontDatabase)
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QSizePolicy, QSlider)

# ── Palette ───────────────────────────────────────────────────────────────────
OW_ORANGE  = QColor("#E89030")
OW_BLUE    = QColor("#4A96CC")
OW_BG      = QColor(13, 10, 26, 220)      # very dark purple, ~86% opaque
OW_BORDER  = QColor(232, 144, 48, 140)    # orange at ~55 %
OW_TEXT_DIM = QColor(160, 140, 100)

# ── Shared font helper ────────────────────────────────────────────────────────
def ow_font(size: int = 11, bold: bool = False) -> QFont:
    """Return a font that resembles the game's clean sans-serif look."""
    f = QFont("Segoe UI", size)
    f.setBold(bold)
    return f


class _CloseButton(QPushButton):
    """Small × close button in the panel header."""

    def __init__(self, parent=None):
        super().__init__("✕", parent)
        self.setFixedSize(22, 22)
        self.setFont(ow_font(9))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #E89030;
                border: 1px solid #E8903055;
                border-radius: 11px;
            }
            QPushButton:hover {
                background: #E8903030;
                border-color: #E89030;
            }
            QPushButton:pressed {
                background: #E8903060;
            }
        """)


class BasePanel(QWidget):
    """
    Frameless floating panel base.

    Sub-classes should:
      • call super().__init__(title, parent)
      • call self._body_layout   to add their content widgets
      • not override paintEvent (background is drawn here)
    """

    closed = pyqtSignal()

    # Minimum / default size — subclasses may override
    _MIN_W = 260
    _MIN_H = 80

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent,
                         Qt.WindowType.Tool |
                         Qt.WindowType.FramelessWindowHint |
                         Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMinimumWidth(self._MIN_W)

        self._drag_pos = None
        self._build_chrome(title)

    # ── chrome (header + body container) ──────────────────────────────

    def _build_chrome(self, title: str) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(14, 10, 14, 14)
        root.setSpacing(8)

        # Header row: title + close button
        header = QHBoxLayout()
        header.setSpacing(6)

        lbl = QLabel(title)
        lbl.setFont(ow_font(12, bold=True))
        lbl.setStyleSheet(f"color: {OW_ORANGE.name()}; background: transparent;")
        header.addWidget(lbl)
        header.addStretch()

        btn = _CloseButton()
        btn.clicked.connect(self._dismiss)
        header.addWidget(btn)

        root.addLayout(header)

        # Thin separator line
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background: {OW_BORDER.name()};")
        root.addWidget(sep)

        # Body: subclasses add rows here
        self._body_layout = QVBoxLayout()
        self._body_layout.setSpacing(10)
        root.addLayout(self._body_layout)

    # ── paint semi-transparent background + orange border ─────────────

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = self.rect().adjusted(1, 1, -1, -1)
        radius = 8.0

        # Background fill
        painter.setBrush(QBrush(OW_BG))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(r, radius, radius)

        # Orange border
        pen = QPen(OW_BORDER)
        pen.setWidthF(1.5)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(r, radius, radius)

    # ── drag-to-move ──────────────────────────────────────────────────

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    # ── keyboard ──────────────────────────────────────────────────────

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self._dismiss()
        else:
            super().keyPressEvent(event)

    # ── dismiss ───────────────────────────────────────────────────────

    def _dismiss(self) -> None:
        self.closed.emit()
        self.close()

    # ── convenience: styled label helpers ────────────────────────────

    # ── shared slider helpers ─────────────────────────────────────────

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

    def _add_slider_row(self, section: str, lo: int, hi: int,
                        step: int, value: int, unit: str = "",
                        on_change=None) -> QSlider:
        """Add labelled slider + range hint to _body_layout; return the QSlider."""
        self._body_layout.addWidget(self._orange_label(section, size=10))

        row = QHBoxLayout()
        row.setSpacing(8)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(lo, hi)
        slider.setSingleStep(step)
        slider.setPageStep(max(step * 5, 1))
        slider.setValue(value)
        slider.setStyleSheet(self._slider_style())
        slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        def _fmt(v: int) -> str:
            return f"{v} {unit}".strip() if unit else str(v)

        val_lbl = self._blue_label(_fmt(value), size=10)
        val_lbl.setFixedWidth(52)
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        slider.valueChanged.connect(lambda v: val_lbl.setText(_fmt(v)))

        row.addWidget(slider)
        row.addWidget(val_lbl)
        self._body_layout.addLayout(row)

        hint = QHBoxLayout()
        lo_lbl = QLabel(_fmt(lo))
        hi_lbl = QLabel(_fmt(hi))
        for lbl in (lo_lbl, hi_lbl):
            lbl.setFont(ow_font(8))
            lbl.setStyleSheet("color: #7060A0; background: transparent;")
        hint.addWidget(lo_lbl)
        hint.addStretch()
        hint.addWidget(hi_lbl)
        self._body_layout.addLayout(hint)

        if on_change:
            slider.valueChanged.connect(on_change)

        return slider

    @staticmethod
    def _orange_label(text: str, size: int = 10) -> QLabel:
        lbl = QLabel(text)
        lbl.setFont(ow_font(size))
        lbl.setStyleSheet(f"color: {OW_ORANGE.name()}; background: transparent;")
        return lbl

    @staticmethod
    def _blue_label(text: str, size: int = 10) -> QLabel:
        lbl = QLabel(text)
        lbl.setFont(ow_font(size))
        lbl.setStyleSheet(f"color: {OW_BLUE.name()}; background: transparent;")
        return lbl

"""
Render diagnostic — 3 layers of visibility test.
If you see: bright purple background + yellow circle + white text → rendering works.
If you see: gray/white Qt default → scene not rendering.
If you see: black → stylesheet override killing rendering.
"""
import sys, os
os.environ.setdefault("QT_QPA_PLATFORM", "xcb")

from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QColor, QBrush, QPen, QFont, QPainter

class TestScene(QGraphicsScene):
    def drawBackground(self, painter, rect):
        print(f"drawBackground called! rect={rect}")
        # Very obvious background — bright purple fill
        painter.fillRect(rect, QColor(120, 0, 180))
        # White circle outline to show scene origin
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(0, 0), 200.0, 200.0)

app = QApplication(sys.argv)
print(f"Platform: {app.platformName()}")

scene = TestScene()
scene.setSceneRect(-300, -300, 600, 600)

# Big yellow circle at centre
sun = QGraphicsEllipseItem(-40, -40, 80, 80)
sun.setBrush(QBrush(QColor(255, 220, 0)))
sun.setPen(QPen(Qt.PenStyle.NoPen))
scene.addItem(sun)

# Red rectangle so we know items render
box = QGraphicsRectItem(100, -20, 80, 40)
box.setBrush(QBrush(QColor(255, 50, 50)))
scene.addItem(box)

# White text
txt = QGraphicsTextItem("RENDER TEST")
txt.setDefaultTextColor(QColor(255, 255, 255))
txt.setFont(QFont("Arial", 20, QFont.Weight.Bold))
txt.setPos(-80, 60)
scene.addItem(txt)

print(f"Scene items: {len(scene.items())}")

view = QGraphicsView(scene)
view.setRenderHint(QPainter.RenderHint.Antialiasing)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
view.setFrameShape(QGraphicsView.Shape.NoFrame)
# No stylesheet — let Qt use defaults so we can see if content renders
view.setWindowTitle("RENDER TEST")
view.resize(600, 600)
view.fitInView(scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
view.show()
view.raise_()
view.activateWindow()

# Re-fit after show (in case layout changed)
QTimer.singleShot(100, lambda: view.fitInView(scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio))
QTimer.singleShot(100, lambda: print(f"After show — view size: {view.width()}x{view.height()}"))

QTimer.singleShot(12000, app.quit)
sys.exit(app.exec())

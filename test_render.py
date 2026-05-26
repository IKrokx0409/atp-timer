import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QBrush, QPen, QFont

app = QApplication(sys.argv)

scene = QGraphicsScene()
scene.setSceneRect(-300, -300, 600, 600)
scene.setBackgroundBrush(QBrush(QColor(10, 4, 20)))

# 黄色太阳
sun = QGraphicsEllipseItem(-25, -25, 50, 50)
sun.setBrush(QBrush(QColor(255, 220, 50)))
sun.setPen(QPen(Qt.PenStyle.NoPen))
scene.addItem(sun)

# 绿色行星
planet = QGraphicsEllipseItem(-15, -15, 30, 30)
planet.setBrush(QBrush(QColor(50, 200, 80)))
planet.setPos(150, 0)
scene.addItem(planet)

# 文字
txt = QGraphicsTextItem("ATP TIMER - can you see me?")
txt.setDefaultTextColor(QColor(255, 255, 255))
txt.setFont(QFont("Arial", 16))
txt.setPos(-130, 60)
scene.addItem(txt)

view = QGraphicsView(scene)
view.setStyleSheet("background: #000010; border: none;")
view.setWindowTitle("ATP Timer Test")
view.resize(600, 600)
view.fitInView(scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
view.show()
view.raise_()

print(f"scene items: {len(scene.items())}, platform: {app.platformName()}")

QTimer.singleShot(10000, app.quit)
sys.exit(app.exec())

import sys
import os

# Force X11/XCB backend — Wayland doesn't support frameless window positioning.
# WSLg exposes XWayland on DISPLAY=:0, so this always works in WSL2.
os.environ.setdefault("QT_QPA_PLATFORM", "xcb")

from PyQt6.QtWidgets import QApplication

from core.config import Config
from ui.window   import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("ATP Timer")

    config = Config("config.json")
    window = MainWindow(config)
    window.show()
    window.raise_()
    window.activateWindow()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

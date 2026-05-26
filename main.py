import sys
import os

# On Linux/WSL force xcb (X11) — Wayland doesn't support frameless window positioning.
# On Windows Qt auto-selects the "windows" plugin, so we only set this on Linux.
if sys.platform.startswith("linux"):
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

import sys
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

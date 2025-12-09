from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme
import sys

from app.ui.main_windw import MainWindow


def main():
    app = QApplication(sys.argv)
    setTheme(Theme.AUTO)

    win = MainWindow()
    win.resize(900, 600)
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
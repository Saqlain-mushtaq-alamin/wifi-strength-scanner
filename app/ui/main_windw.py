from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
)
from qfluentwidgets import PrimaryPushButton

from app.ui.widgets.blueprint_viewer import BlueprintViewer
from app.ui.scan_page import ScanPage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("WiFi Strength Scanner(wfss)")
        self._setup_ui()

    def _setup_ui(self):
        # Keep a reference to the current central content
        self.central_container = QWidget()
        self.setCentralWidget(self.central_container)

        self.main_layout = QVBoxLayout(self.central_container)

        # Initial landing view
        self.blueprint_viewer = BlueprintViewer()
        self.main_layout.addWidget(self.blueprint_viewer)

        # Buttons Layout (centered)
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        load_button = PrimaryPushButton("Scan Blueprint")
        load_button.setFixedSize(150, 100)
        load_button.clicked.connect(self.open_scan_page)
        buttons_layout.addWidget(load_button)

        

        buttons_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)
        self.main_layout.addSpacing(200)  # Fixed space in pixels

    def open_scan_page(self):
        # Replace the central content with ScanPage
        scan_page = ScanPage(self)
        self.setCentralWidget(scan_page)


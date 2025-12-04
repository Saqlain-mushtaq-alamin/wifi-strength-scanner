from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from qfluentwidgets import PrimaryPushButton

from app.ui.widgets.blueprint_viewer import BlueprintViewer
from app.ui.scan_page import ScanPage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("WiFi Strength Scanner (wfss)")
        self._setup_ui()

    def _setup_ui(self):
        # Central container
        self.central_container = QWidget()
        self.setCentralWidget(self.central_container)

        #  apply background style
        




        self.main_layout = QVBoxLayout(self.central_container)

        # =========================================================
        # TITLE SECTION — stays at the top
        # =========================================================

        title_widget = QWidget()
        title_widget.setObjectName("TitleWidget")

        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(20, 40, 20, 40)
        title_layout.setSpacing(10)

        # Main Title
        title_label = QLabel("wfss")
        title_label.setStyleSheet("""
            font-size: 56px;
            font-weight: bold;
            color: #e0e7ff;
            text-shadow: 0px 2px 10px rgba(59, 130, 246, 0.5);
            letter-spacing: 2px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        subtitle_label = QLabel("WiFi Strength Scanner")
        subtitle_label.setStyleSheet("""
            font-size: 18px;
            color: #bfdbfe;
            font-weight: 500;
            letter-spacing: 1px;
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)

        title_widget.setStyleSheet("""
            #TitleWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3b82f6,
                    stop:0.5 #1e40af,
                    stop:1 #0c1117);
                border: none;
                border-bottom: 2px solid rgba(59, 130, 246, 0.4);
                border-bottom-left-radius: 50px;
                border-bottom-right-radius: 50px;
            }
        """)

        # Add title to the top
        self.main_layout.addWidget(title_widget)
        self.main_layout.addSpacing(40)

        # =========================================================
        # BLUEPRINT VIEWER (now under the title)
        # =========================================================

        self.blueprint_viewer = BlueprintViewer()
        self.main_layout.addWidget(self.blueprint_viewer)
        self.main_layout.addSpacing(40)

        # =========================================================
        # BUTTONS SECTION
        # =========================================================

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        button_style = """
PrimaryPushButton {
    background: rgba(20, 25, 30, 0.35);
    color: #dceaff;
    font-size: 18px;
    font-weight: 600;
    padding: 12px;
    border-radius: 18px;
    border: 1px solid rgba(0, 98, 255, 0.4);
    backdrop-filter: blur(25px);
    box-shadow: 
        0 0 12px rgba(0, 115, 255, 0.35),
        inset 0 -2px 6px rgba(0, 0, 0, 0.4),
        inset 0 2px 6px rgba(255, 255, 255, 0.06);
}

PrimaryPushButton:hover {
    background: rgba(30, 40, 60, 0.55);
    border: 1px solid rgba(0, 140, 255, 0.9);
    color: #e8f3ff;
    box-shadow: 
        0 0 20px rgba(0, 132, 255, 0.8),
        0 0 40px rgba(0, 132, 255, 0.6);
    transform: translateY(-2px);
}

PrimaryPushButton:pressed {
    background: rgba(15, 20, 25, 0.8);
    box-shadow: 0 0 10px rgba(0, 100, 255, 0.4);
    transform: scale(0.96);
}
"""

        load_button = PrimaryPushButton("Scan Blueprint")
        load_button.setFixedSize(150, 100)
        load_button.setStyleSheet(button_style)
        load_button.clicked.connect(self.open_scan_page)
        buttons_layout.addWidget(load_button)

        heatmap_button = PrimaryPushButton("Heatmap List")
        heatmap_button.setFixedSize(150, 100)
        heatmap_button.setStyleSheet(button_style)
        heatmap_button.clicked.connect(self.open_heatmap_list)
        buttons_layout.addWidget(heatmap_button)

        buttons_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)
        self.main_layout.addSpacing(200) 


    # =========================================================
    # PAGE SWITCHING
    # =========================================================
    def open_scan_page(self):
        scan_page = ScanPage(self)
        self.setCentralWidget(scan_page)

    def open_heatmap_list(self):
        pass  # Add later

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from qfluentwidgets import PrimaryPushButton

from app.ui.widgets.blueprint_viewer import BlueprintViewer
from app.ui.scan_page import ScanPage
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient
from PySide6.QtCore import QRectF, QPointF, Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget


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
 


        # Create a widget container for everything except the title
        self.main_layout = QVBoxLayout(self.central_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

 

        # =========================================================
        # TITLE SECTION — stays at the top
        # =========================================================

        class SciFiTitle(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setObjectName("SciFiTitle")
                self.setFixedHeight(180)

                # Content layout
                title_layout = QVBoxLayout(self)
                title_layout.setContentsMargins(24, 24, 24, 24)
                title_layout.setSpacing(6)

                title_label = QLabel("wfss", self)
                title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                title_label.setStyleSheet("""
                    color: #e6f2ff;
                    font-size: 64px;
                    font-weight: 900;
                    letter-spacing: 3px;
                """)

                subtitle_label = QLabel("WiFi Strength Scanner", self)
                subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                subtitle_label.setStyleSheet("""
                    color: #a8caff;
                    font-size: 18px;
                    font-weight: 600;
                    letter-spacing: 1.2px;
                """)

                title_layout.addStretch()
                title_layout.addWidget(title_label)
                title_layout.addWidget(subtitle_label)
                title_layout.addStretch()

                # extra CSS for subtle inner glow of labels
                self.setStyleSheet("""
                    #SciFiTitle QLabel {
                        background: transparent;
                    }
                """)

            def paintEvent(self, event):
                p = QPainter(self)
                p.setRenderHint(QPainter.RenderHint.Antialiasing)

                r = self.rect().adjusted(10, 6, -10, -6)

                # 3D beveled base plate
                base_grad = QLinearGradient(r.topLeft(), r.bottomRight())
                base_grad.setColorAt(0.0, QColor(12, 18, 30, 255))
                base_grad.setColorAt(0.35, QColor(16, 26, 48, 255))
                base_grad.setColorAt(0.7, QColor(10, 20, 38, 255))
                base_grad.setColorAt(1.0, QColor(8, 14, 26, 255))
                p.setBrush(QBrush(base_grad))
                p.setPen(QPen(QColor(0, 120, 255, 100), 1.4))
                p.drawRoundedRect(r, 28, 28)

                # Rim highlight (fake 3D bevel)
                rim_r = r.adjusted(2, 2, -2, -2)
                rim_grad = QLinearGradient(rim_r.topLeft(), rim_r.bottomRight())
                rim_grad.setColorAt(0.0, QColor(0, 180, 255, 50))
                rim_grad.setColorAt(0.5, QColor(0, 140, 255, 18))
                rim_grad.setColorAt(1.0, QColor(0, 220, 255, 60))
                p.setBrush(QBrush(rim_grad))
                p.setPen(QPen(QColor(0, 170, 255, 90), 1))
                p.drawRoundedRect(rim_r, 26, 26)

                # Holographic diagonal sheen
                sheen = QLinearGradient(r.topLeft(), r.bottomRight())
                sheen.setColorAt(0.0, QColor(0, 0, 0, 0))
                sheen.setColorAt(0.45, QColor(80, 200, 255, 28))
                sheen.setColorAt(0.55, QColor(255, 255, 255, 30))
                sheen.setColorAt(0.65, QColor(80, 200, 255, 28))
                sheen.setColorAt(1.0, QColor(0, 0, 0, 0))
                p.setBrush(QBrush(sheen))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawRoundedRect(r.adjusted(4, 4, -4, -4), 24, 24)

                # Neon top accent line
                p.setPen(QPen(QColor(0, 190, 255, 200), 2.2))
                p.drawLine(r.left() + 20, r.top() + 12, r.right() - 20, r.top() + 12)

                # Circuit grid pattern
                grid_pen = QPen(QColor(0, 160, 255, 60), 1)
                p.setPen(grid_pen)
                step = 42
                for x in range(int(r.left()) + 28, int(r.right()) - 28, step):
                    p.drawLine(x, r.top() + 26, x + 36, r.bottom() - 26)
                for y in range(int(r.top()) + 30, int(r.bottom()) - 30, step):
                    p.drawLine(r.left() + 24, y, r.right() - 24, y - 18)

                # Nodes / LEDs
                p.setPen(Qt.PenStyle.NoPen)
                for i in range(8):
                    px = r.left() + 60 + i * step
                    py = r.top() + 40 + (i % 3) * 18
                    p.setBrush(QColor(120, 210, 255, 190))
                    p.drawEllipse(QPointF(px, py), 3.6, 3.6)
                    p.setBrush(QColor(0, 170, 255, 70))
                    p.drawEllipse(QRectF(px - 10, py - 6, 20, 12))

                # Bottom glow bar
                glow_r = QRectF(r.left() + 20, r.bottom() - 24, r.width() - 40, 10)
                glow_grad = QLinearGradient(glow_r.topLeft(), glow_r.bottomRight())
                glow_grad.setColorAt(0.0, QColor(0, 120, 255, 0))
                glow_grad.setColorAt(0.5, QColor(0, 180, 255, 180))
                glow_grad.setColorAt(1.0, QColor(0, 120, 255, 0))
                p.setBrush(QBrush(glow_grad))
                p.drawRoundedRect(glow_r, 8, 8)

                # Corner crystal accents
                p.setBrush(QColor(0, 160, 255, 55))
                p.drawEllipse(QRectF(r.left() + 18, r.top() + 18, 22, 22))
                p.drawEllipse(QRectF(r.right() - 40, r.top() + 18, 22, 22))

        title_widget = SciFiTitle(self)
        self.main_layout.addWidget(title_widget)
        self.main_layout.addSpacing(40)

        # =========================================================
        # BLUEPRINT VIEWER (now under the title)
        # =========================================================

        self.blueprint_viewer = BlueprintViewer()
        self.main_layout.addWidget(self.blueprint_viewer)
        self.main_layout.addSpacing(20)

        # =========================================================
        # BUTTONS SECTION
        # =========================================================

        # Container with sci‑fi glassy background and border
        # Wrapper to center the fixed-size container horizontally
        buttons_container = QWidget()  # wrapper
        wrapper_layout = QHBoxLayout(buttons_container)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.addStretch()

        # Actual styled panel
        panel = QWidget()
        panel.setObjectName("ButtonsContainer")
        panel.setFixedSize(600, 200)   # width, height

        buttons_container_layout = QHBoxLayout(panel)
        buttons_container_layout.setContentsMargins(20, 20, 20, 20)
        buttons_container_layout.setSpacing(0)

        wrapper_layout.addWidget(panel, 0, Qt.AlignmentFlag.AlignCenter)
        wrapper_layout.addStretch()


        # Style the container (Qt "CSS")
        buttons_container.setStyleSheet("""
    #ButtonsContainer {
        border: 1px solid rgba(0, 150, 255, 120);
        border-top-color: rgba(0, 180, 255, 160);
        border-bottom-color: rgba(0, 110, 220, 100);
        border-radius: 26px;
    }

    #ButtonsContainer::hover {
        border-color: rgba(0, 190, 255, 180);
    }

    /* subtle inner highlight using padding + gradient child hack */
    #ButtonsContainer > * {
        background: transparent;
    }

    /* Neon diagonal accent lines using a gradient overlay-like effect */
    #ButtonsContainer {
        /* fake glow edges */
        outline: none;
    }
    """)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(30)
        buttons_layout.addStretch()

        button_style = """
    PrimaryPushButton {
        background: rgba(20, 25, 30, 0.35);
        color: #dceaff;
        font-size: 18px;
        font-weight: 600;
        padding: 12px;
        border-radius: 18px;
        border: 1px solid rgba(0, 98, 255, 0.55);
    }

    PrimaryPushButton:hover {
        background: rgba(30, 40, 60, 0.55);
        border: 1px solid rgba(0, 160, 255, 0.95);
        color: #e8f3ff;
    }

    PrimaryPushButton:pressed {
        background: rgba(15, 20, 25, 0.85);
        border: 1px solid rgba(0, 140, 255, 0.9);
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

        speedtest_button = PrimaryPushButton("Speed Test")
        speedtest_button.setFixedSize(150, 100)
        speedtest_button.setStyleSheet(button_style)
        speedtest_button.clicked.connect(self.open_speed_test)
        buttons_layout.addWidget(speedtest_button)

        buttons_layout.addStretch()

        # Add the buttons layout into the styled container
        buttons_container_layout.addLayout(buttons_layout)

        # Place the container in the main layout
        self.main_layout.addWidget(buttons_container)
        self.main_layout.addSpacing(150)
        # extra spacing between buttons handled by layout spacing above


        # =========================================================
        # FOOTER SECTION
        # =========================================================
        class SciFiFooter(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setFixedHeight(140)
                self.setObjectName("SciFiFooter")

                root = QHBoxLayout(self)
                root.setContentsMargins(24, 18, 24, 18)
                root.setSpacing(18)

                left_box = QWidget(self)
                left_layout = QVBoxLayout(left_box)
                left_layout.setContentsMargins(0, 0, 0, 0)
                left_layout.setSpacing(6)

                title = QLabel("wfss")
                title.setStyleSheet("font-size: 18px; font-weight: 700; color: #bcd7ff; letter-spacing: 1px;")
                subtitle = QLabel("WiFi Strength Scanner")
                subtitle = QLabel("saqlain • farhan • tamim • govt")
                subtitle.setStyleSheet("color: #8fb4ff; font-size: 12px;")

                left_layout.addWidget(title)
                left_layout.addWidget(subtitle)

                right_chip = QLabel("Gang Bangers", self)
                right_chip.setStyleSheet("""
                    padding: 6px 12px;
                    color: #e7f1ff;
                    background-color: rgba(30, 50, 80, 0.35);
                    border: 1px solid rgba(0, 155, 255, 0.55);
                    border-radius: 12px;
                """)

                root.addWidget(left_box)
                root.addStretch()
                root.addWidget(right_chip)

                self.setStyleSheet("""
                    #SciFiFooter {
                        border-top-left-radius: 22px;
                        border-top-right-radius: 22px;
                        border: 1px solid rgba(0, 120, 255, 0.35);
                        background: transparent;
                    }
                """)

            def paintEvent(self, event):
                p = QPainter(self)
                p.setRenderHint(QPainter.RenderHint.Antialiasing)

                r = self.rect().adjusted(8, 6, -8, -8)

                # Glassy background
                grad = QLinearGradient(r.topLeft(), r.bottomRight())
                grad.setColorAt(0.0, QColor(10, 18, 30, 190))
                grad.setColorAt(0.5, QColor(14, 24, 44, 180))
                grad.setColorAt(1.0, QColor(18, 28, 54, 200))
                p.setBrush(QBrush(grad))
                p.setPen(QPen(QColor(0, 120, 255, 90), 1.2))
                p.drawRoundedRect(r, 20, 20)

                # Neon top highlight
                p.setPen(QPen(QColor(0, 160, 255, 180), 2))
                p.drawLine(r.left() + 14, r.top() + 12, r.right() - 14, r.top() + 12)

                # Sci‑fi pattern: diagonal circuits and grid
                grid_pen = QPen(QColor(0, 190, 255, 70), 1)
                p.setPen(grid_pen)
                step = 44
                for x in range(int(r.left()) + 24, int(r.right()), step):
                    p.drawLine(x, r.top() + 26, x + 30, r.bottom() - 26)
                for y in range(int(r.top()) + 26, int(r.bottom()), step):
                    p.drawLine(r.left() + 24, y, r.right() - 24, y - 18)

                # Nodes
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(QColor(120, 210, 255, 170))
                for i in range(7):
                    px = r.left() + 60 + i * step
                    py = r.top() + 30 + (i % 3) * 20
                    p.drawEllipse(QPointF(px, py), 3.2, 3.2)

                # Soft corner glow
                p.setBrush(QColor(0, 140, 255, 50))
                p.drawEllipse(QRectF(r.right() - 130, r.center().y() - 45, 110, 90))

        self.main_layout.addStretch()
        self.footer = SciFiFooter(self)
        self.main_layout.addWidget(self.footer)
    


    # =========================================================
    # PAGE SWITCHING
    # =========================================================
    def open_scan_page(self):
        scan_page = ScanPage(self)
        self.setCentralWidget(scan_page)

    def open_heatmap_list(self):
        pass  # Add later

    def open_speed_test(self):
        # Placeholder page until Speed Test implementation exists
        placeholder = QWidget(self)
        layout = QVBoxLayout(placeholder)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        label = QLabel("Speed Test page is under construction.", placeholder)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setCentralWidget(placeholder)

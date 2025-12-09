from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from qfluentwidgets import PrimaryPushButton


class SpeedTestPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._timer = QTimer(self)
        self._timer.setInterval(60)
        self._timer.timeout.connect(self._tick)
        self._target = 0.0
        self._value = 0.0
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)
        #====================================================
        # Header section        
        #====================================================

        # Header container with a narrow height
        header = QWidget(self)
        header.setObjectName("headerContainer")
        header.setFixedHeight(36)  # very narrow
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 4, 8, 4)
        header_layout.setSpacing(6)

        # Glassy look with top/bottom borders
        header.setStyleSheet("""
        #headerContainer {
            background: rgba(30, 36, 42, 140);  /* glassy translucent */
            border-top: 1px solid rgba(120, 200, 255, 160);
            border-bottom: 1px solid rgba(120, 200, 255, 160);
        }
        #headerContainer:hover {
            background: rgba(36, 42, 48, 170);
            border-top: 1px solid rgba(120, 200, 255, 220);
            border-bottom: 1px solid rgba(120, 200, 255, 220);
        }
        """)

        # Subtle shadow for depth
        shadow = QGraphicsDropShadowEffect(header)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(80, 140, 200, 160))
        header.setGraphicsEffect(shadow)

        # Back button on the left
        self.back_btn = PrimaryPushButton("Back", header)
        self.back_btn.setObjectName("backBtn")
        self.back_btn.setFixedHeight(28)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setStyleSheet("""
        #backBtn {
            background: transparent;
            border: none;
            border-right: 1px solid rgba(120, 200, 255, 180);
            color: #d7eaff;
            padding: 0 10px;  /* added padding */
        }
        #backBtn:hover {
            background: rgba(30, 36, 42, 120);  /* hover effect */
            border-right: 1px solid rgba(120, 200, 255, 220);
        }
        #backBtn:pressed {
            background: rgba(21, 212, 253, 80); /* pressed effect */
            border-right: 1px solid rgba(120, 200, 255, 255);
        }
        """)

        self.back_btn.clicked.connect(self._go_back)
        header_layout.addWidget(self.back_btn, 0, Qt.AlignmentFlag.AlignLeft)
        header_layout.addStretch(1)

        # Add header to the top (non-expanding)
        root.addWidget(header, 0)


        # Speed readout
        self.readout = QLabel("0.0 Mbps")
        rf = QFont("Segoe UI", 32, QFont.Weight.Bold)
        self.readout.setFont(rf)
        self.readout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.readout, 1)

        # Start button (bigger, classic look, hover/click effects with speed vibe)
        self.start_btn = PrimaryPushButton("Start Speed Test", self)
        self.start_btn.setObjectName("startBtn")
        self.start_btn.setMinimumSize(260, 52)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet("""
        #startBtn {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(0, 160, 255, 230),
                        stop:1 rgba(0, 255, 200, 230));
            color: #eaf7ff;
            border: 2px solid rgba(0, 210, 255, 200);
            border-radius: 10px;
            padding: 10px 26px;
            font-size: 16px;
            font-weight: 600;
        }
        #startBtn:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(0, 190, 255, 255),
                        stop:1 rgba(0, 255, 220, 255));
            border: 2px solid rgba(0, 240, 255, 230);
            color: #ffffff;
        }
        #startBtn:pressed {
            background: qlineargradient(x1:1, y1:0, x2:0, y2:0,
                        stop:0 rgba(0, 150, 230, 230),
                        stop:1 rgba(0, 225, 190, 230));
            border: 2px solid rgba(120, 255, 255, 255);
            padding-top: 12px;      /* subtle press depth */
            padding-bottom: 8px;
        }
        """)
        # Neon-ish glow that intensifies on hover/press
        _btnGlow = QGraphicsDropShadowEffect(self.start_btn)
        _btnGlow.setBlurRadius(18)
        _btnGlow.setOffset(0, 4)
        _btnGlow.setColor(QColor(0, 190, 255, 120))
        self.start_btn.setGraphicsEffect(_btnGlow)

        def _enter(e):
            _btnGlow.setBlurRadius(28)
            _btnGlow.setOffset(0, 6)
            _btnGlow.setColor(QColor(0, 220, 255, 170))
            type(self.start_btn).enterEvent(self.start_btn, e)

        def _leave(e):
            _btnGlow.setBlurRadius(18)
            _btnGlow.setOffset(0, 4)
            _btnGlow.setColor(QColor(0, 190, 255, 120))
            type(self.start_btn).leaveEvent(self.start_btn, e)

        def _pressed():
            _btnGlow.setBlurRadius(14)
            _btnGlow.setOffset(0, 2)

        def _released():
            _btnGlow.setBlurRadius(28)
            _btnGlow.setOffset(0, 6)

        self.start_btn.enterEvent = _enter
        self.start_btn.leaveEvent = _leave
        self.start_btn.pressed.connect(_pressed)
        self.start_btn.released.connect(_released)

        self.start_btn.clicked.connect(self.start_test)
        root.addWidget(self.start_btn, 0, Qt.AlignmentFlag.AlignHCenter)

        root.addStretch(1)

    def _go_back(self):
        try:
            from importlib import import_module
            MainWindow = None
            for mod in ("app.ui.main_windw", "app.ui.main_window"):
                try:
                    MainWindow = getattr(import_module(mod), "MainWindow")
                    break
                except Exception:
                    continue
            top = self.window()
            if MainWindow is not None and isinstance(top, MainWindow):
                rebuild = getattr(top, "_setup_ui", None)
                if callable(rebuild):
                    rebuild()
                    return
        except Exception:
            pass

    def start_test(self):
        # Simple simulated test: animate up to a random target
        import random
        self.start_btn.setDisabled(True)
        self._value = 0.0
        self._target = random.uniform(50.0, 450.0)
        self._timer.start()

    def _tick(self):
        # Ease toward target and update readout
        step = max(1.0, (self._target - self._value) * 0.12)
        self._value = min(self._target, self._value + step)
        self.readout.setText(f"{self._value:,.1f} Mbps")
        if abs(self._target - self._value) < 0.5:
            self._timer.stop()
            self.start_btn.setDisabled(False)
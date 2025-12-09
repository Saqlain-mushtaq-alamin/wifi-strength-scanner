from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QRadioButton, QButtonGroup
)
from PySide6.QtGui import QDoubleValidator
from app.core.scanner import WifiScanner


class WiFiInputDialog(QDialog):
    """Dialog to choose between automatic WiFi scan or manual RSSI input."""

    def __init__(self, parent=None, x=0, y=0, edit_mode=False, current_rssi=None):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.edit_mode = edit_mode
        self.current_rssi = current_rssi
        self.rssi_value = None
        self.wifi_info = None

        self.setWindowTitle("Edit WiFi Scan Point" if edit_mode else "WiFi Scan Options")
        self.setModal(True)
        self.setMinimumWidth(400)

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        if self.edit_mode:
            title = QLabel(f"Edit WiFi Scan Point ({self.x:.1f}, {self.y:.1f})")
            if self.current_rssi is not None:
                title.setText(title.text() + f"\nCurrent RSSI: {self.current_rssi:.0f} dBm")
        else:
            title = QLabel(f"Add WiFi Scan Point ({self.x:.1f}, {self.y:.1f})")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #e6edf3;")
        layout.addWidget(title)

        # Radio button group for mode selection
        mode_label = QLabel("Select input method:")
        mode_label.setStyleSheet("color: #d7eaff;")
        layout.addWidget(mode_label)

        self.button_group = QButtonGroup(self)

        self.auto_radio = QRadioButton("Auto-scan WiFi (use current connection)" if not self.edit_mode else "Rescan WiFi")
        self.auto_radio.setChecked(True)
        self.auto_radio.setStyleSheet("color: #d7eaff;")
        self.button_group.addButton(self.auto_radio)
        layout.addWidget(self.auto_radio)

        self.manual_radio = QRadioButton("Manual input (enter RSSI value)")
        self.manual_radio.setStyleSheet("color: #d7eaff;")
        self.button_group.addButton(self.manual_radio)
        layout.addWidget(self.manual_radio)

        # Manual input field
        manual_container = QHBoxLayout()
        manual_container.setSpacing(10)

        rssi_label = QLabel("RSSI:")
        rssi_label.setStyleSheet("color: #d7eaff;")
        manual_container.addWidget(rssi_label)

        self.rssi_input = QLineEdit()
        self.rssi_input.setPlaceholderText("e.g., -45")
        # Pre-fill with current RSSI in edit mode
        if self.edit_mode and self.current_rssi is not None:
            self.rssi_input.setText(str(int(self.current_rssi)))
        self.rssi_input.setEnabled(False)
        validator = QDoubleValidator(-100.0, 0.0, 2)
        self.rssi_input.setValidator(validator)
        manual_container.addWidget(self.rssi_input)

        layout.addLayout(manual_container)

        # Enable/disable manual input based on radio selection
        self.auto_radio.toggled.connect(self._on_mode_changed)

        # Info text area
        info_text = "Click OK to rescan WiFi automatically" if self.edit_mode else "Click OK to scan WiFi automatically"
        self.info_label = QLabel(info_text)
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet(
            "color: #9fb0c0; font-size: 11px; "
            "background: rgba(30, 36, 42, 140); "
            "border: 1px solid rgba(120, 200, 255, 60); "
            "border-radius: 6px; padding: 8px;"
        )
        layout.addWidget(self.info_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()

        self.ok_btn = QPushButton("Update" if self.edit_mode else "OK")
        self.ok_btn.setFixedWidth(100)
        self.ok_btn.clicked.connect(self._on_ok_clicked)
        button_layout.addWidget(self.ok_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedWidth(100)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

    def _on_mode_changed(self, checked):
        """Enable/disable manual input field based on mode."""
        self.rssi_input.setEnabled(not checked)
        if checked:
            if self.edit_mode:
                self.info_label.setText("Click Update to rescan WiFi automatically")
            else:
                self.info_label.setText("Click OK to scan WiFi automatically")
        else:
            self.info_label.setText("Enter RSSI value (typically between -30 to -90)")

    def _on_ok_clicked(self):
        """Process the input based on selected mode."""
        if self.auto_radio.isChecked():
            # Auto-scan mode
            try:
                self.wifi_info = WifiScanner.scan()
                if self.wifi_info and isinstance(self.wifi_info, dict):
                    self.rssi_value = self.wifi_info.get("rssi")
                    if self.rssi_value is None:
                        self.info_label.setText("Error: Could not retrieve RSSI from WiFi scan")
                        self.info_label.setStyleSheet(
                            "color: #ff6b6b; font-size: 11px; "
                            "background: rgba(60, 36, 42, 140); "
                            "border: 1px solid rgba(255, 100, 100, 160); "
                            "border-radius: 6px; padding: 8px;"
                        )
                        return
                    self.accept()
                else:
                    self.info_label.setText("Error: WiFi scan failed")
                    self.info_label.setStyleSheet(
                        "color: #ff6b6b; font-size: 11px; "
                        "background: rgba(60, 36, 42, 140); "
                        "border: 1px solid rgba(255, 100, 100, 160); "
                        "border-radius: 6px; padding: 8px;"
                    )
            except Exception as e:
                self.info_label.setText(f"Error: {str(e)}")
                self.info_label.setStyleSheet(
                    "color: #ff6b6b; font-size: 11px; "
                    "background: rgba(60, 36, 42, 140); "
                    "border: 1px solid rgba(255, 100, 100, 160); "
                    "border-radius: 6px; padding: 8px;"
                )
        else:
            # Manual input mode
            text = self.rssi_input.text().strip()
            if not text:
                self.info_label.setText("Please enter an RSSI value")
                self.info_label.setStyleSheet(
                    "color: #ff6b6b; font-size: 11px; "
                    "background: rgba(60, 36, 42, 140); "
                    "border: 1px solid rgba(255, 100, 100, 160); "
                    "border-radius: 6px; padding: 8px;"
                )
                return

            try:
                self.rssi_value = float(text)
                # Create basic wifi_info dict for manual input
                self.wifi_info = {
                    "rssi": self.rssi_value,
                    "ssid": "Manual Input",
                    "bssid": "N/A",
                    "signal": None,
                    "channel": None,
                    "radio": None,
                    "band": None
                }
                self.accept()
            except ValueError:
                self.info_label.setText("Invalid RSSI value")
                self.info_label.setStyleSheet(
                    "color: #ff6b6b; font-size: 11px; "
                    "background: rgba(60, 36, 42, 140); "
                    "border: 1px solid rgba(255, 100, 100, 160); "
                    "border-radius: 6px; padding: 8px;"
                )

    def _apply_styles(self):
        """Apply dark theme styling to the dialog."""
        self.setStyleSheet("""
            QDialog {
                background: #0f1318;
                color: #e6edf3;
            }
            QPushButton {
                background: rgba(30, 36, 42, 220);
                color: #d7eaff;
                border: 1px solid rgba(120, 200, 255, 120);
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: rgba(40, 50, 60, 240);
                border: 1px solid rgba(120, 200, 255, 200);
            }
            QPushButton:pressed {
                background: rgba(20, 26, 32, 240);
            }
            QLineEdit {
                background: rgba(30, 36, 42, 170);
                color: #cfe7ff;
                border: 1px solid rgba(120, 200, 255, 80);
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(120, 200, 255, 180);
            }
            QRadioButton {
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid rgba(120, 200, 255, 120);
                background: rgba(30, 36, 42, 170);
            }
            QRadioButton::indicator:checked {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                    fx:0.5, fy:0.5,
                    stop:0 rgba(0, 190, 255, 255),
                    stop:0.6 rgba(0, 190, 255, 255),
                    stop:1 rgba(30, 36, 42, 170));
            }
        """)


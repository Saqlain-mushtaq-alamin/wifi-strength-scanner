from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect, QCheckBox
from qfluentwidgets import PrimaryPushButton


class SpeedTestThread(QThread):
    """Background thread for running speed test without blocking UI."""
    progress = Signal(str)  # Progress messages
    finished = Signal(dict)  # Final results: {download, upload, ping}
    error = Signal(str)  # Error message

    def __init__(self, run_multiple=False):
        super().__init__()
        self._is_cancelled = False
        self._run_multiple = run_multiple

    def cancel(self):
        """Request cancellation of the speed test."""
        self._is_cancelled = True

    def run(self):
        try:
            if self._is_cancelled:
                return

            self.progress.emit("Initializing speed test...")
            import speedtest
            import socket

            # Set a reasonable timeout for socket operations
            socket.setdefaulttimeout(15)

            if self._is_cancelled:
                return

            # Use secure connection and configure for better reliability
            st = speedtest.Speedtest(secure=True)

            if self._is_cancelled:
                return

            self.progress.emit("Finding best server...")
            # Get best server - this is where it often hangs
            st.get_best_server()

            if self._run_multiple:
                # Run 3 tests and average
                num_tests = 3
                download_results = []
                upload_results = []
                ping_results = []

                for i in range(num_tests):
                    if self._is_cancelled:
                        return

                    self.progress.emit(f"Test {i+1}/{num_tests}: Testing download speed...")
                    download_bps = st.download(threads=None)
                    download_mbps = download_bps / 1_000_000
                    download_results.append(download_mbps)

                    if self._is_cancelled:
                        return

                    self.progress.emit(f"Test {i+1}/{num_tests}: Testing upload speed...")
                    upload_bps = st.upload(threads=None, pre_allocate=False)
                    upload_mbps = upload_bps / 1_000_000
                    upload_results.append(upload_mbps)
                    ping_results.append(st.results.ping)

                    # Small delay between tests
                    if i < num_tests - 1:
                        self.msleep(1000)

                # Average the results
                download_mbps = sum(download_results) / len(download_results)
                upload_mbps = sum(upload_results) / len(upload_results)
                ping = sum(ping_results) / len(ping_results)

            else:
                # Single test
                if self._is_cancelled:
                    return

                self.progress.emit("Testing download speed...")
                download_bps = st.download(threads=None)
                download_mbps = download_bps / 1_000_000  # Convert to Mbps

                if self._is_cancelled:
                    return

                self.progress.emit("Testing upload speed...")
                upload_bps = st.upload(threads=None, pre_allocate=False)
                upload_mbps = upload_bps / 1_000_000  # Convert to Mbps

                if self._is_cancelled:
                    return

                ping = st.results.ping

            results = {
                'download': download_mbps,
                'upload': upload_mbps,
                'ping': ping
            }

            if not self._is_cancelled:
                self.finished.emit(results)

        except Exception as e:
            if not self._is_cancelled:
                import traceback
                error_detail = traceback.format_exc()
                print(f"Speed test error details:\n{error_detail}")
                self.error.emit(f"Speed test failed: {str(e)}")


class SpeedTestPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._test_thread = None
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

        # Speed readout labels
        info_container = QWidget(self)
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(15)

        # Status label
        self.status_label = QLabel("Ready to test")
        self.status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #9fb0c0;")
        info_layout.addWidget(self.status_label)

        # Download speed
        self.download_label = QLabel("Download: -- Mbps")
        self.download_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.download_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_label.setStyleSheet("color: #21d4fd;")
        info_layout.addWidget(self.download_label)

        # Upload speed
        self.upload_label = QLabel("Upload: -- Mbps")
        self.upload_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.upload_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_label.setStyleSheet("color: #b721ff;")
        info_layout.addWidget(self.upload_label)

        # Ping
        self.ping_label = QLabel("Ping: -- ms")
        self.ping_label.setFont(QFont("Segoe UI", 18))
        self.ping_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ping_label.setStyleSheet("color: #d7eaff;")
        info_layout.addWidget(self.ping_label)

        # Multiple tests checkbox
        self.multi_test_checkbox = QCheckBox("Run 3 tests and average (more consistent results)")
        self.multi_test_checkbox.setFont(QFont("Segoe UI", 10))
        self.multi_test_checkbox.setStyleSheet("""
            QCheckBox {
                color: #9fb0c0;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid rgba(120, 200, 255, 160);
                border-radius: 4px;
                background: rgba(30, 36, 42, 140);
            }
            QCheckBox::indicator:checked {
                background: rgba(33, 212, 253, 200);
                border: 2px solid rgba(33, 212, 253, 220);
            }
            QCheckBox::indicator:hover {
                border: 2px solid rgba(120, 200, 255, 220);
            }
        """)
        info_layout.addWidget(self.multi_test_checkbox, 0, Qt.AlignmentFlag.AlignCenter)

        root.addWidget(info_container, 1)

        # Buttons container
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Start button (bigger, classic look, hover/click effects with speed vibe)
        self.start_btn = PrimaryPushButton("Start Speed Test", self)
        self.start_btn.setObjectName("startBtn")
        self.start_btn.setMinimumSize(220, 52)
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
        #startBtn:disabled {
            background: rgba(100, 100, 100, 150);
            border: 2px solid rgba(120, 120, 120, 150);
            color: rgba(200, 200, 200, 150);
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

        # Cancel button
        self.cancel_btn = PrimaryPushButton("Cancel", self)
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setMinimumSize(120, 52)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setVisible(False)  # Hidden by default
        self.cancel_btn.setStyleSheet("""
        #cancelBtn {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(255, 80, 80, 230),
                        stop:1 rgba(255, 120, 120, 230));
            color: #ffffff;
            border: 2px solid rgba(255, 100, 100, 200);
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 600;
        }
        #cancelBtn:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(255, 100, 100, 255),
                        stop:1 rgba(255, 140, 140, 255));
            border: 2px solid rgba(255, 120, 120, 230);
        }
        #cancelBtn:pressed {
            background: qlineargradient(x1:1, y1:0, x2:0, y2:0,
                        stop:0 rgba(230, 70, 70, 230),
                        stop:1 rgba(230, 100, 100, 230));
            border: 2px solid rgba(255, 140, 140, 255);
            padding-top: 12px;
            padding-bottom: 8px;
        }
        """)
        self.cancel_btn.clicked.connect(self.cancel_test)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addStretch()

        root.addLayout(buttons_layout, 0)

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
        """Start the speed test in a background thread."""
        if self._test_thread is not None and self._test_thread.isRunning():
            return  # Test already running

        # Reset display
        self.download_label.setText("Download: -- Mbps")
        self.upload_label.setText("Upload: -- Mbps")
        self.ping_label.setText("Ping: -- ms")
        self.status_label.setText("Starting test...")

        # Update buttons
        self.start_btn.setDisabled(True)
        self.start_btn.setText("Testing...")
        self.cancel_btn.setVisible(True)
        self.multi_test_checkbox.setDisabled(True)

        # Create and start thread with multiple test option
        run_multiple = self.multi_test_checkbox.isChecked()
        self._test_thread = SpeedTestThread(run_multiple=run_multiple)
        self._test_thread.progress.connect(self._on_progress)
        self._test_thread.finished.connect(self._on_test_finished)
        self._test_thread.error.connect(self._on_test_error)
        self._test_thread.start()

    def cancel_test(self):
        """Cancel the running speed test."""
        if self._test_thread is not None and self._test_thread.isRunning():
            self.status_label.setText("Cancelling test...")
            self._test_thread.cancel()
            self._test_thread.quit()
            self._test_thread.wait(2000)  # Wait up to 2 seconds
            if self._test_thread.isRunning():
                self._test_thread.terminate()  # Force terminate if still running

            self.status_label.setText("Test cancelled")
            self._reset_buttons()

    def _reset_buttons(self):
        """Reset button states after test completion or cancellation."""
        self.start_btn.setDisabled(False)
        self.start_btn.setText("Start Speed Test")
        self.cancel_btn.setVisible(False)
        self.multi_test_checkbox.setDisabled(False)

    def _on_progress(self, message: str):
        """Update status label with progress message."""
        self.status_label.setText(message)

    def _on_test_finished(self, results: dict):
        """Handle test completion with results."""
        download = results['download']
        upload = results['upload']
        ping = results['ping']

        self.download_label.setText(f"Download: {download:.2f} Mbps")
        self.upload_label.setText(f"Upload: {upload:.2f} Mbps")
        self.ping_label.setText(f"Ping: {ping:.1f} ms")
        self.status_label.setText("Test complete!")

        # Re-enable button
        self._reset_buttons()

        print(f"Speed test results - Download: {download:.2f} Mbps, Upload: {upload:.2f} Mbps, Ping: {ping:.1f} ms")

    def _on_test_error(self, error_msg: str):
        """Handle test error."""
        self.status_label.setText(f"Error: {error_msg}")
        self.download_label.setText("Download: Error")
        self.upload_label.setText("Upload: Error")
        self.ping_label.setText("Ping: Error")

        # Re-enable button
        self._reset_buttons()

        print(f"Speed test error: {error_msg}")


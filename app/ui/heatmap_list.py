from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QAbstractItemView,
    QLabel, QFrame, QSizePolicy, QStackedWidget, QApplication, QPushButton
)

class HeatmapList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.HeatmapListPage()
        self.apply_styles()

    def HeatmapListPage(self):
        root = QVBoxLayout()
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Header
        header = QFrame()
        header.setMinimumHeight(64)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 12, 12, 12)
        header_layout.setSpacing(8)

        title = QLabel("Wi‑Fi Heatmaps")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
     
         # Back button on the left
        self.back_btn = QPushButton("Back", header)
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

        def _go_back():
            try:
                # Resolve MainWindow class (prefer main_windw.py, fallback to main_window.py)
                from importlib import import_module
                MainWindow = None
                for mod in ("app.ui.main_windw", "app.ui.main_window"):
                    try:
                        MainWindow = getattr(import_module(mod), "MainWindow")
                        break
                    except Exception:
                        continue

                top = self.window()

                # If embedded inside MainWindow, rebuild its landing view in-place
                if MainWindow is not None and isinstance(top, MainWindow):
                    try:
                        # Recreate the main landing UI (title, viewer, buttons)
                        rebuild = getattr(top, "_setup_ui", None)
                        if callable(rebuild):
                            rebuild()
                            return
                    except Exception:
                        pass

                    # Fallback: try to locate a QStackedWidget and go to index 0
                    parent = self.parentWidget()
                    while parent is not None and not isinstance(parent, QStackedWidget):
                        parent = parent.parentWidget()
                    if isinstance(parent, QStackedWidget):
                        parent.setCurrentIndex(0)
                        return

                # Otherwise, show or create the main window and close this standalone window
                app = QApplication.instance()
                mw = None
                if isinstance(app, QApplication) and MainWindow is not None:
                    mw = next((w for w in app.topLevelWidgets() if isinstance(w, MainWindow)), None)
                    if mw is None:
                        mw = MainWindow()
                if mw is not None:
                    mw.show()
                    try:
                        mw.raise_()
                        mw.activateWindow()
                    except Exception:
                        pass
                if top is not mw and hasattr(top, "close"):
                    top.close()
            except Exception as e:
                print(f"Back navigation failed: {e}")

        self.back_btn.clicked.connect(_go_back)
        header_layout.addWidget(self.back_btn, 0, Qt.AlignmentFlag.AlignLeft)
        header_layout.addStretch(1)


        header_layout.addWidget(title)
 
        root.addWidget(header)

        # Main content split: left list (≈30%), right blueprint + footer (≈70%)
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left bar: heatmap list (constrained width to approximate 30%)
        left = QFrame()
        left.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        left.setMinimumWidth(280)  # tweak as needed
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        left_header = QLabel("Heatmap Sets")
        left_header.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))

        self.heatmap_list_widget = QListWidget()
        self.heatmap_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.heatmap_list_widget.itemClicked.connect(self.on_heatmap_selected)
        self.heatmap_list_widget.setObjectName("heatmapList")

        left_layout.addWidget(left_header)
        left_layout.addWidget(self.heatmap_list_widget)

        # Right bar: blueprint + footer
        right = QFrame()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(8)

        blueprint_header = QLabel("Blueprint Preview")
        blueprint_header.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))

        self.blueprint_view = QLabel("No blueprint loaded")
        self.blueprint_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blueprint_view.setObjectName("blueprintView")
        self.blueprint_view.setMinimumHeight(240)
        footer = QLabel("Tip: Select a heatmap to preview its blueprint and coverage.")
        footer.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        footer.setObjectName("footer")
        footer.setMinimumHeight(60)

        right_layout.addWidget(blueprint_header)
        right_layout.addWidget(self.blueprint_view, 1)
        right_layout.addWidget(footer)

        content.addWidget(left, 7)   # ~70%
        content.addWidget(right, 3)  # ~30%
        root.addLayout(content)

        self.setLayout(root)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background: #0f1318;
                color: #e6edf3;
            }
            QFrame {
                background: #151a21;
                border: 1px solid #222935;
                border-radius: 10px;
            }
            QLabel {
                color: #e6edf3;
            }
            QListWidget#heatmapList {
                background: #0f1318;
                border: 1px solid #222935;
                border-radius: 8px;
                padding: 6px;
            }
            QListWidget#heatmapList::item {
                padding: 8px;
                margin: 2px 0;
            }
            QListWidget#heatmapList::item:selected {
                background: #2a3442;
                border-radius: 6px;
            }
            QLabel#blueprintView {
                background: #0f1318;
                border: 1px dashed #334052;
                border-radius: 8px;
            }
            QLabel#footer {
                color: #9fb0c0;
                font-size: 11px;
            }
        """)

    def on_heatmap_selected(self, item):
        # Update blueprint preview when a heatmap is selected.
        self.blueprint_view.setText(f"Preview: {item.text()}")

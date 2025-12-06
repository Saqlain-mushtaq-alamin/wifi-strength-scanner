from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QAbstractItemView,
    QLabel, QFrame, QSizePolicy
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
        subtitle = QLabel("Scan, visualize, and refine your coverage")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        subtitle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
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

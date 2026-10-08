from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OSRS Profit Advisor")
        self.resize(1280, 860)
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(
            """
            QMainWindow {
                background: #e7e7e7;
                border: 1px solid #2a2a2a;
            }
            QWidget {
                color: #1a1a1a;
                font-family: 'Segoe UI', sans-serif;
            }
            """
        )

        container = QWidget(self)
        container.setStyleSheet("background: #e7e7e7;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(34)
        header.setStyleSheet(
            "background: #2b2b2b; border: 1px solid #1d1d1d; border-bottom: 0;"
        )
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(14, 0, 14, 0)
        header_layout.setSpacing(0)

        title = QLabel("OSRS Profit Advisor")
        title.setStyleSheet(
            "color: #f3f3f3; font-weight: 600; font-size: 14px; margin-left: 8px;"
        )
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(title)
        header_layout.addStretch()

        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(10)

        for text in ["_", "□", "×"]:
            btn = QLabel(text)
            btn.setAlignment(Qt.AlignCenter)
            btn.setStyleSheet(
                "color: #f0f0f0; background: transparent; font-size: 16px; font-weight: 600;"
            )
            controls_layout.addWidget(btn)
        header_layout.addWidget(controls)

        layout.addWidget(header)

        workspace = QWidget()
        workspace.setStyleSheet("background: #e7e7e7; border: 1px solid #2d2d2d; border-top: 0;")
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)

        spacer_top = QWidget()
        spacer_top.setFixedHeight(60)
        spacer_top.setStyleSheet("background: transparent;")
        workspace_layout.addWidget(spacer_top)

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 0, 0, 0)
        content_layout.setSpacing(0)

        app_title = QLabel("OSRS Profit Advisor")
        app_title.setStyleSheet("font-size: 28px; color: #1e1e1e; font-weight: 400;")
        content_layout.addWidget(app_title)

        content_layout.addStretch()

        status = QLabel("Phase 2: live API integration and data synchronization layer initialized.")
        status.setStyleSheet("font-size: 20px; color: #1e1e1e; font-weight: 400;")
        status.setWordWrap(True)
        status.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        content_layout.addWidget(status)

        workspace_layout.addWidget(content)
        layout.addWidget(workspace)

        self.setCentralWidget(container)


def main() -> int:
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

from __future__ import annotations

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OSRS Profit Advisor")
        self.resize(1200, 800)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        title = QLabel("OSRS Profit Advisor")
        title.setStyleSheet("font-size: 22px; font-weight: 600;")
        layout.addWidget(title)

        status = QLabel("Phase 1: application scaffold and calculation layer initialized.")
        status.setWordWrap(True)
        layout.addWidget(status)

        self.setCentralWidget(central_widget)


def main() -> int:
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

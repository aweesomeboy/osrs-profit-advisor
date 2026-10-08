from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OSRS Profit Advisor")
        self.resize(1300, 820)
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(
            """
            QMainWindow { background: #f2f2f2; }
            QWidget { font-family: 'Segoe UI', sans-serif; }
            QLabel { color: #1d1d1d; }
            QTabWidget::pane { border: 1px solid #d0d0d0; background: white; }
            QTabBar::tab { background: #e8e8e8; color: #1d1d1d; padding: 10px 18px; }
            QTabBar::tab:selected { background: white; border: 1px solid #d0d0d0; border-bottom: none; }
            QTableWidget { gridline-color: #d8d8d8; background: white; }
            QHeaderView::section { background: #ededed; color: #222; padding: 6px; }
            """
        )

        tabs = QTabWidget(self)
        tabs.addTab(self._create_dashboard_tab(), "Dashboard")
        tabs.addTab(self._create_item_search_tab(), "Item Search")
        tabs.addTab(self._create_recipe_tab(), "Recipe Scanner")
        tabs.addTab(self._create_forecast_tab(), "Price Forecast")
        tabs.addTab(self._create_settings_tab(), "Settings")

        self.setCentralWidget(tabs)

    def _create_dashboard_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(14)

        summary = QWidget()
        summary_layout = QHBoxLayout(summary)
        for label, value in [
            ("Last sync", "09:45"),
            ("Loaded items", "1,240"),
            ("Top recipes", "12"),
            ("Sync errors", "0"),
        ]:
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card.setStyleSheet("background: #f7f7f7; border: 1px solid #d9d9d9; border-radius: 8px;")
            title = QLabel(label)
            title.setStyleSheet("font-size: 11px; color: #555;")
            value_label = QLabel(value)
            value_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #1b1b1b;")
            card_layout.addWidget(title)
            card_layout.addWidget(value_label)
            summary_layout.addWidget(card)
        layout.addWidget(summary)

        table = QTableWidget(5, 5)
        table.setHorizontalHeaderLabels(["Recipe", "Profit", "ROI", "Volume", "Risk"])
        table.setRowCount(5)
        rows = [
            ("Magic log", "2,340,400", "34.1%", "7,200", "Stable"),
            ("Manta ray", "1,770,000", "18.9%", "3,900", "Stable"),
            ("Coal bag", "980,000", "11.3%", "2,800", "Medium"),
            ("Bronze bar", "-540,000", "-8.4%", "1,400", "Low"),
            ("Prayer potion", "2,110,000", "27.7%", "6,100", "Stable"),
        ]
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
        layout.addWidget(table)
        return widget

    def _create_item_search_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        search_row = QWidget()
        search_layout = QHBoxLayout(search_row)
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by item name...")
        search_layout.addWidget(search_input)
        layout.addWidget(search_row)

        table = QTableWidget(8, 9)
        table.setHorizontalHeaderLabels([
            "Name",
            "Item ID",
            "High",
            "Low",
            "Avg",
            "Updated",
            "Volume",
            "Spread",
            "ROI",
        ])
        table.setRowCount(8)
        rows = [
            ("Rune essence", "537", "198", "192", "195", "2 min ago", "201k", "6", "4.8%"),
            ("Lobster", "379", "860", "830", "845", "4 min ago", "93k", "30", "6.3%"),
            ("Mithril bar", "2351", "1,460", "1,410", "1,435", "6 min ago", "42k", "50", "8.1%"),
            ("Dragon claws", "14484", "3,800", "3,620", "3,710", "9 min ago", "11k", "180", "13.2%"),
            ("Coal", "4540", "210", "204", "207", "1 min ago", "440k", "6", "2.5%"),
            ("Air rune", "556", "40", "39", "39.5", "1 min ago", "1.2m", "1", "1.9%"),
            ("Gold bar", "2357", "1,080", "1,040", "1,060", "10 min ago", "2.3k", "40", "6.6%"),
            ("Cannonball", "2", "128", "121", "123", "2 min ago", "450k", "7", "4.0%"),
        ]
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
        layout.addWidget(table)
        return widget

    def _create_recipe_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.addWidget(QLabel("Skill:"))
        skill_box = QComboBox()
        skill_box.addItems(["All", "Cooking", "Smithing", "Mining", "Fishing", "Runecrafting"])
        controls_layout.addWidget(skill_box)
        controls_layout.addStretch()
        search = QLineEdit()
        search.setPlaceholderText("Filter recipes...")
        controls_layout.addWidget(search)
        layout.addWidget(controls)

        table = QTableWidget(6, 6)
        table.setHorizontalHeaderLabels(["Recipe", "Skill", "Profit", "ROI", "Time", "Volume"])
        table.setRowCount(6)
        rows = [
            ("Cooked Karambwan", "Cooking", "2,440,000", "28.4%", "60s", "11k"),
            ("Mithril platebody", "Smithing", "1,180,000", "19.7%", "120s", "8.7k"),
            ("Runite ore", "Mining", "940,000", "17.9%", "90s", "4k"),
            ("Salmon", "Fishing", "660,000", "15.2%", "30s", "9.1k"),
            ("Nature rune", "Runecrafting", "820,000", "14.4%", "45s", "6.4k"),
            ("Bronze dagger", "Smithing", "-90,000", "-3.1%", "30s", "2.8k"),
        ]
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
        layout.addWidget(table)
        return widget

    def _create_forecast_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form = QFormLayout()
        item_combo = QComboBox()
        item_combo.addItems(["Rune essence", "Lobster", "Mithril bar", "Dragon claws", "Coal"])
        period_combo = QComboBox()
        period_combo.addItems(["24h", "3d", "7d"])
        form.addRow("Item:", item_combo)
        form.addRow("Period:", period_combo)
        layout.addLayout(form)

        forecast_box = QWidget()
        forecast_layout = QVBoxLayout(forecast_box)
        forecast_layout.addWidget(QLabel("Forecast for 24h: 2,460,000 – 2,570,000 GP"))
        forecast_layout.addWidget(QLabel("Trend: upward"))
        forecast_layout.addWidget(QLabel("Expected change: +3.8%"))
        forecast_layout.addWidget(QLabel("Confidence: medium | dataset quality: 14 samples"))
        forecast_layout.addWidget(QLabel("Warning: volume is moderate, so estimate is not high confidence."))
        layout.addWidget(forecast_box)
        return widget

    def _create_settings_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form = QFormLayout()
        form.addRow("User-Agent:", QLineEdit("OSRSProfitAdvisor/1.0 contact: moj-email@example.com"))
        form.addRow("Refresh interval (min):", QLineEdit("5"))
        form.addRow("Database path:", QLineEdit("data/osrs_profit_advisor.db"))
        form.addRow("Price TTL (min):", QLineEdit("30"))
        form.addRow("Warn on low volume:", QComboBox())
        layout.addLayout(form)
        return widget


def main() -> int:
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

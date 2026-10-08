from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OSRS Profit Advisor")
        self.resize(1400, 900)
        self.setMinimumSize(1100, 720)
        self.setStyleSheet(
            """
            QMainWindow {
                background: #181a1d;
            }
            QWidget {
                color: #f2efe8;
                font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            }
            QPushButton {
                border: 1px solid #3a362e;
                background: #2b2a29;
                color: #f2efe8;
                border-radius: 6px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background: #3a362e;
            }
            QLineEdit, QComboBox {
                background: #202225;
                border: 1px solid #3d3a35;
                border-radius: 6px;
                color: #f2efe8;
                padding: 7px 10px;
            }
            QTableWidget {
                background: #1e2124;
                alternate-background-color: #1a1d20;
                gridline-color: #2f3438;
                color: #f5f2ea;
            }
            QHeaderView::section {
                background: #2a2d30;
                color: #e5d4a2;
                padding: 8px;
                border: 1px solid #3a3f43;
            }
            QTableWidget::item {
                padding: 8px 6px;
            }
            QLabel {
                color: #f2efe8;
            }
            """
        )

        root = QWidget(self)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self._build_sidebar()
        root_layout.addWidget(sidebar, 0)

        content = QWidget()
        content.setStyleSheet("background: #17191c;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        header = self._build_header()
        content_layout.addWidget(header, 0)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_dashboard_page())
        self.stack.addWidget(self._build_ge_prices_page())
        self.stack.addWidget(self._build_flip_finder_page())
        self.stack.addWidget(self._build_recipe_profit_page())
        self.stack.addWidget(self._build_price_charts_page())
        self.stack.addWidget(self._build_price_forecast_page())
        self.stack.addWidget(self._build_settings_page())
        content_layout.addWidget(self.stack, 1)

        status_bar = self._build_status_bar()
        content_layout.addWidget(status_bar, 0)

        root_layout.addWidget(content, 1)
        self.setCentralWidget(root)

    def _build_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(
            """
            background: #1c1e20;
            border-right: 1px solid #2c2d2f;
            """
        )
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 18, 12, 12)
        layout.setSpacing(10)

        title = QLabel("OSRS Profit Advisor")
        title_font = QFont()
        title_font.setPointSize(17)
        title_font.setWeight(QFont.DemiBold)
        title.setFont(title_font)
        title.setStyleSheet("color: #f5d78c; margin-bottom: 12px;")
        layout.addWidget(title)

        self.nav_buttons = []
        nav_items = [
            ("Dashboard", 0),
            ("GE Prices", 1),
            ("Flip Finder", 2),
            ("Recipe Profit", 3),
            ("Price Charts", 4),
            ("Price Forecast", 5),
            ("Settings", 6),
        ]

        for label, index in nav_items:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(
                """
                QPushButton {
                    text-align: left;
                    padding: 10px 12px;
                    border-radius: 7px;
                    border: 1px solid transparent;
                    background: transparent;
                    color: #e8e0d0;
                }
                QPushButton:hover {
                    background: #2a2d30;
                }
                QPushButton:checked {
                    background: #3a2c1f;
                    border: 1px solid #7a5a2a;
                    color: #f5d78c;
                }
                """
            )
            if index == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda _, idx=index: self._select_nav(idx))
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        footer = QLabel("Local-only prototype\nNo account required")
        footer.setStyleSheet("color: #b8b0a1; font-size: 11px; line-height: 1.5;")
        footer.setWordWrap(True)
        layout.addWidget(footer)

        return sidebar

    def _select_nav(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        for btn in self.nav_buttons:
            btn.setChecked(False)
        self.nav_buttons[index].setChecked(True)

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setStyleSheet("background: #1a1d1f; border-bottom: 1px solid #2c2d2f;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 10, 16, 10)
        header_layout.setSpacing(14)

        app_label = QLabel("OSRS Profit Advisor")
        app_font = QFont()
        app_font.setPointSize(15)
        app_font.setWeight(QFont.DemiBold)
        app_label.setFont(app_font)
        app_label.setStyleSheet("color: #f0d9a2;")
        header_layout.addWidget(app_label)
        header_layout.addStretch()

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(
            """
            QPushButton {
                background: #3a2c1f;
                border: 1px solid #7a5a2a;
                color: #f0d9a2;
                padding: 8px 14px;
            }
            QPushButton:hover { background: #4c3c27; }
            """
        )
        header_layout.addWidget(refresh_btn)

        last_sync = QLabel("Last sync: 09:45")
        last_sync.setStyleSheet("color: #d9d1bf; font-size: 12px;")
        header_layout.addWidget(last_sync)

        settings_btn = QPushButton("Settings")
        header_layout.addWidget(settings_btn)

        api_status = QLabel("API: Healthy")
        api_status.setStyleSheet("color: #7ed39a; font-size: 12px; font-weight: 600;")
        header_layout.addWidget(api_status)

        return header

    def _build_status_bar(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(32)
        bar.setStyleSheet("background: #1d2022; border-top: 1px solid #2d3033;")
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(16, 0, 16, 0)

        status = QLabel("Ready • Local data only • No account required")
        status.setStyleSheet("color: #d2d2d2; font-size: 11px;")
        bar_layout.addWidget(status)
        bar_layout.addStretch()

        status_hint = QLabel("Status: Offline-ready")
        status_hint.setStyleSheet("color: #82d58d; font-size: 11px; font-weight: 600;")
        bar_layout.addWidget(status_hint)
        return bar

    def _build_dashboard_page(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: #17191c;")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        cards = QWidget()
        cards_layout = QHBoxLayout(cards)
        cards_layout.setSpacing(14)

        card_specs = [
            ("API Status", "Healthy", "#6bd68e", "Online"),
            ("Tracked Items", "1,240", "#d8b566", "Updated"),
            ("Best Flip", "Manta Ray", "#8ce6b7", "+18.9% ROI"),
            ("Best Recipe", "Magic log", "#d8b566", "+34.1% ROI"),
            ("Last Update", "09:45", "#7fc8ff", "Today"),
        ]

        for title, value, accent, caption in card_specs:
            card = QWidget()
            card.setStyleSheet(
                f"background: #1d2124; border: 1px solid #2d3034; border-radius: 10px;"
            )
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 10, 12, 10)
            card_layout.setSpacing(6)

            label = QLabel(title)
            label.setStyleSheet("color: #bdb7aa; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;")
            value_w = QLabel(value)
            value_font = QFont()
            value_font.setPointSize(19)
            value_font.setWeight(QFont.DemiBold)
            value_w.setFont(value_font)
            value_w.setStyleSheet(f"color: {accent};")
            caption_w = QLabel(caption)
            caption_w.setStyleSheet("color: #a5a39a; font-size: 10px;")

            card_layout.addWidget(label)
            card_layout.addWidget(value_w)
            card_layout.addWidget(caption_w)
            cards_layout.addWidget(card)

        layout.addWidget(cards)

        title = QLabel("Grand Exchange Tracker")
        title_font = QFont(); title_font.setPointSize(17); title_font.setWeight(QFont.DemiBold)
        title.setFont(title_font)
        title.setStyleSheet("color: #f0d9a2; margin-top: 8px;")
        layout.addWidget(title)

        controls = QWidget(); controls_layout = QHBoxLayout(controls); controls_layout.setContentsMargins(0,0,0,0)
        search = QLineEdit(); search.setPlaceholderText("Search item..."); search.setMaximumWidth(260)
        filter_min = QLineEdit(); filter_min.setPlaceholderText("Min profit"); filter_min.setMaximumWidth(130)
        roi_box = QComboBox(); roi_box.addItems(["All ROI", "> 10%", "> 20%", "> 30%"])
        roi_box.setMaximumWidth(140)
        controls_layout.addWidget(search)
        controls_layout.addWidget(filter_min)
        controls_layout.addWidget(roi_box)
        controls_layout.addStretch()
        refresh = QPushButton("Refresh")
        controls_layout.addWidget(refresh)
        layout.addWidget(controls)

        table = QTableWidget(8, 8)
        table.setAlternatingRowColors(True)
        table.setHorizontalHeaderLabels(["Item", "Buy", "Sell", "Margin", "ROI", "Volume", "Trend", "Last update"])
        table.setSortingEnabled(True)
        rows = [
            ("Manta ray", "690", "840", "+150", "21.7%", "12.4k", "Up", "09:32"),
            ("Magic log", "480", "640", "+160", "33.3%", "8.9k", "Up", "09:31"),
            ("Coal bag", "360", "430", "+70", "19.4%", "19.2k", "Stable", "09:29"),
            ("Bronze bar", "180", "205", "+25", "13.9%", "43k", "Stable", "09:27"),
            ("Prayer potion", "310", "420", "+110", "35.5%", "5.1k", "Up", "09:25"),
            ("Rune essence", "24", "29", "+5", "20.8%", "168k", "Down", "09:24"),
            ("Lobster", "820", "900", "+80", "9.8%", "13.7k", "Up", "09:23"),
            ("Mithril bar", "1450", "1560", "+110", "7.6%", "7.4k", "Stable", "09:20"),
        ]
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        layout.addWidget(table)

        footer = QWidget(); footer_layout = QHBoxLayout(footer); footer_layout.setContentsMargins(0,0,0,0)
        results = QLabel("Showing 1–8 of 8 results")
        results.setStyleSheet("color: #c7b89d; font-size: 11px;")
        footer_layout.addWidget(results)
        footer_layout.addStretch()
        next_page = QPushButton("Next page")
        footer_layout.addWidget(next_page)
        layout.addWidget(footer)

        return page

    def _build_ge_prices_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(18,18,18,18); layout.setSpacing(14)

        toolbar = QWidget(); tb = QHBoxLayout(toolbar); tb.setContentsMargins(0,0,0,0)
        search = QLineEdit(); search.setPlaceholderText("Search by item name / ID"); search.setMaximumWidth(420)
        tb.addWidget(search)
        tb.addStretch()
        tb.addWidget(QPushButton("Export CSV"))
        layout.addWidget(toolbar)

        table = QTableWidget(10, 8)
        table.setAlternatingRowColors(True)
        table.setHorizontalHeaderLabels(["Item", "High", "Low", "Margin", "Buy limit", "Volume", "Updated", "Trend"])
        rows = [
            ("Rune essence", "198", "192", "+6", "100k", "201k", "09:41", "Stable"),
            ("Air rune", "40", "39", "+1", "500k", "1.2m", "09:39", "Down"),
            ("Lobster", "860", "830", "+30", "30k", "93k", "09:33", "Up"),
            ("Mithril bar", "1460", "1410", "+50", "20k", "42k", "09:30", "Up"),
            ("Dragon claws", "3800", "3620", "+180", "8k", "11k", "09:26", "Up"),
            ("Coal", "210", "204", "+6", "100k", "440k", "09:25", "Stable"),
            ("Magic log", "640", "480", "+160", "15k", "8.9k", "09:23", "Up"),
            ("Manta ray", "840", "690", "+150", "7k", "12.4k", "09:22", "Up"),
            ("Prayer potion", "420", "310", "+110", "10k", "5.1k", "09:21", "Up"),
            ("Bronze bar", "205", "180", "+25", "35k", "43k", "09:19", "Stable"),
        ]
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
        table.doubleClicked.connect(lambda _ : self._select_nav(1))
        layout.addWidget(table)
        return page

    def _build_flip_finder_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(18,18,18,18); layout.setSpacing(16)

        filters = QWidget(); filters.setStyleSheet("background: #1d2124; border: 1px solid #303538; border-radius: 8px;")
        filters_layout = QHBoxLayout(filters)
        filters_layout.setSpacing(14)
        filter_fields = [
            ("Budget", QLineEdit("500000")),
            ("Min ROI", QLineEdit("10%")),
            ("Min Profit", QLineEdit("20000")),
            ("Min Volume", QLineEdit("5000")),
            ("Max Buy", QLineEdit("1500")),
        ]
        for title, widget in filter_fields:
            box = QWidget(); box_layout = QVBoxLayout(box); box_layout.setContentsMargins(0,0,0,0)
            label = QLabel(title); label.setStyleSheet("color: #d7caa1; font-size: 11px;")
            widget.setMaximumWidth(140)
            box_layout.addWidget(label); box_layout.addWidget(widget); filters_layout.addWidget(box)
        chk = QWidget(); chk_layout = QVBoxLayout(chk); chk_layout.setContentsMargins(0,0,0,0)
        chk_label = QLabel("Stable only"); chk_label.setStyleSheet("color: #d7caa1; font-size: 11px;")
        combo = QComboBox(); combo.addItems(["Yes", "No"])
        combo.setMaximumWidth(120)
        chk_layout.addWidget(chk_label); chk_layout.addWidget(combo); filters_layout.addWidget(chk)
        filters_layout.addStretch()
        filters_layout.addWidget(QPushButton("Apply"))
        layout.addWidget(filters)

        table = QTableWidget(6, 10)
        table.setHorizontalHeaderLabels(["Item", "Buy", "Sell", "Margin", "Margin after tax", "ROI", "Volume", "Buy limit", "Profit @ budget", "Risk"])
        rows = [
            ("Manta ray", "690", "840", "+150", "+132", "21.7%", "12.4k", "7k", "+182k", "Low"),
            ("Magic log", "480", "640", "+160", "+140", "33.3%", "8.9k", "15k", "+150k", "Low"),
            ("Coal bag", "360", "430", "+70", "+58", "19.4%", "19.2k", "50k", "+92k", "Medium"),
            ("Prayer potion", "310", "420", "+110", "+98", "35.5%", "5.1k", "10k", "+130k", "Low"),
            ("Bronze bar", "180", "205", "+25", "+20", "13.9%", "43k", "35k", "+62k", "Low"),
        ]
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
        layout.addWidget(table)
        return page

    def _build_recipe_profit_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(18,18,18,18); layout.setSpacing(14)

        controls = QWidget(); c = QHBoxLayout(controls); c.setContentsMargins(0,0,0,0); c.setSpacing(10)
        search = QLineEdit(); search.setPlaceholderText("Search recipe..."); search.setMaximumWidth(260)
        c.addWidget(search)
        c.addWidget(QPushButton("Add Recipe"))
        c.addWidget(QPushButton("Refresh Prices"))
        budget = QLineEdit("500000"); budget.setMaximumWidth(120)
        min_profit = QLineEdit("20000"); min_profit.setMaximumWidth(120)
        c.addWidget(QLabel("Budget")); c.addWidget(budget)
        c.addWidget(QLabel("Min profit")); c.addWidget(min_profit)
        c.addStretch()
        layout.addWidget(controls)

        table = QTableWidget(6, 10)
        table.setHorizontalHeaderLabels(["Recipe", "Material cost", "Output value", "GE tax", "Net profit", "ROI", "Profit/hr", "Volume", "Risk", "Last update"])
        rows = [
            ("Cooked Karambwan", "1,740,000", "4,180,000", "70,000", "+2,370,000", "136%", "+28,000/hr", "11k", "Low", "09:48"),
            ("Mithril platebody", "1,820,000", "3,000,000", "95,000", "+1,085,000", "59%", "+17,000/hr", "8.7k", "Low", "09:46"),
            ("Runite ore", "890,000", "1,830,000", "48,000", "+892,000", "100%", "+15,000/hr", "4k", "Medium", "09:44"),
            ("Salmon", "540,000", "1,210,000", "12,000", "+658,000", "122%", "+21,000/hr", "9.1k", "Low", "09:41"),
            ("Nature rune", "910,000", "1,730,000", "26,000", "+794,000", "87%", "+11,000/hr", "6.4k", "Low", "09:39"),
            ("Bronze dagger", "490,000", "420,000", "18,000", "−88,000", "−18%", "−3,000/hr", "2.8k", "High", "09:38"),
        ]
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        table.resizeColumnsToContents()
        layout.addWidget(table)
        return page

    def _build_price_charts_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(18,18,18,18); layout.setSpacing(14)

        toolbar = QWidget(); tl = QHBoxLayout(toolbar); tl.setContentsMargins(0,0,0,0); tl.setSpacing(12)
        item_search = QLineEdit(); item_search.setPlaceholderText("Search item"); item_search.setMaximumWidth(260)
        interval = QComboBox(); interval.addItems(["1D", "7D", "30D", "90D"])
        tl.addWidget(item_search); tl.addWidget(interval); tl.addStretch(); tl.addWidget(QPushButton("Apply"))
        layout.addWidget(toolbar)

        chart_panel = QWidget(); chart_panel.setStyleSheet("background: #1d2124; border: 1px solid #2f3438; border-radius: 10px;")
        chart_panel_layout = QVBoxLayout(chart_panel); chart_panel_layout.setContentsMargins(16,16,16,16)
        chart_panel_title = QLabel("Price history: Manta ray")
        chart_panel_title.setStyleSheet("color: #f0d9a2; font-weight: 600;")
        chart_panel_layout.addWidget(chart_panel_title)

        chart_placeholder = QLabel("[ Price chart placeholder ]\n\n7-day and 30-day moving averages shown with volume bars.")
        chart_placeholder.setStyleSheet("background: #161a1d; border: 1px solid #2b2f33; border-radius: 8px; color: #dfe6d4; padding: 16px; min-height: 180px;")
        chart_placeholder.setAlignment(Qt.AlignCenter)
        chart_panel_layout.addWidget(chart_placeholder)

        volume_box = QWidget(); volume_box.setStyleSheet("background: #15191c; border: 1px solid #2b2f33; border-radius: 8px;")
        volume_layout = QHBoxLayout(volume_box); volume_layout.setContentsMargins(16,12,16,12)
        for val, label in [(10, "Mon"), (30, "Tue"), (50, "Wed"), (65, "Thu"), (80, "Fri"), (45, "Sat"), (70, "Sun")]:
            bar = QFrame(); bar.setFixedHeight(90); bar.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d8b566, stop:1 #6d4f24); max-width: 28px; min-width: 24px; border-radius: 4px;");
            bar.setProperty("height", val)
            stack = QVBoxLayout(); stack.setContentsMargins(0,0,0,0); stack.addStretch(); stack.addWidget(bar); stack.addWidget(QLabel(label))
            volume_layout.addLayout(stack)
        chart_panel_layout.addWidget(volume_box)
        layout.addWidget(chart_panel)
        return page

    def _build_price_forecast_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(18,18,18,18); layout.setSpacing(16)

        cards = QWidget(); cards_layout = QHBoxLayout(cards); cards_layout.setSpacing(14)
        metrics = [
            ("Current Price", "840 GP"),
            ("24h Forecast", "+58 GP"),
            ("3d Forecast", "+180 GP"),
            ("7d Forecast", "+420 GP"),
        ]
        for title, value in metrics:
            card = QWidget(); card.setStyleSheet("background: #1d2124; border: 1px solid #303538; border-radius: 8px;")
            c = QVBoxLayout(card); c.setContentsMargins(12,10,12,10)
            c.addWidget(QLabel(title))
            v = QLabel(value); v.setStyleSheet("color: #7ed39a; font-size: 22px; font-weight: 600;"); c.addWidget(v)
            cards_layout.addWidget(card)
        layout.addWidget(cards)

        forecast_panel = QWidget(); forecast_panel.setStyleSheet("background: #1d2124; border: 1px solid #303538; border-radius: 8px;")
        forecast_layout = QVBoxLayout(forecast_panel); forecast_layout.setContentsMargins(18,18,18,18); forecast_layout.setSpacing(10)

        forecast_layout.addWidget(QLabel("Forecast outlook"))
        forecast_layout.addWidget(QLabel("Trend: Favorable"))
        forecast_layout.addWidget(QLabel("Confidence: Medium"))
        forecast_layout.addWidget(QLabel("Price range: 785 – 910 GP"))
        forecast_layout.addWidget(QLabel("Data points used: 42"))
        forecast_layout.addWidget(QLabel("Recommendation: Neutral to favorable, with moderate volatility."))

        layout.addWidget(forecast_panel)
        return page

    def _build_settings_page(self) -> QWidget:
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(18,18,18,18); layout.setSpacing(16)
        card = QWidget(); card.setStyleSheet("background: #1d2124; border: 1px solid #303538; border-radius: 10px;")
        form = QFormLayout(card); form.setContentsMargins(18,18,18,18); form.setSpacing(12)

        form.addRow("Refresh interval", QLineEdit("5 min"))
        form.addRow("Default budget", QLineEdit("500000"))
        form.addRow("Default min ROI", QLineEdit("10%"))
        form.addRow("Local data path", QLineEdit("~/osrs_profit_advisor/data"))
        form.addRow("Price timeout", QLineEdit("15 sec"))
        form.addRow("Theme", QComboBox())
        form.widgetGenerator()
        layout.addWidget(card)
        save = QPushButton("Save settings")
        layout.addWidget(save)
        return page


def main() -> int:
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

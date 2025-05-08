import sys
import os
import json
from datetime import datetime, timedelta, date
from calendar import monthrange
import sys, os, json
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QComboBox, QGridLayout, QFrame, QMessageBox
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt

DATA_FILE = 'data.json'

data = {}
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # Empty or corrupt file — reinitialize
        data = {}
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

class CounterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Tracker")
        self.setMinimumSize(800, 750)
        self.current_date = datetime.today().replace(day=1)

        self.is_dark_mode = True
        self.selected_counter = ""

        self.init_ui()
        self.refresh_counter_menu()
        self.update_today_label()
        self.draw_calendar()

    def init_ui(self):
        main = QWidget()
        self.setCentralWidget(main)
        self.layout = QVBoxLayout(main)

        title_label = QLabel("Daily Tracker")
        title_label.setFont(QFont("Segoe UI", 30, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label, alignment=Qt.AlignCenter)
        font = QFont("Segoe UI", 20)
        header_font = QFont("Segoe UI", 26, QFont.Bold)

        main = QWidget()
        self.setCentralWidget(main)
        self.layout = QVBoxLayout(main)

        # Dropdown
        self.counter_dropdown = QComboBox()
        self.counter_dropdown.setFont(QFont("Segoe UI", 18))
        self.counter_dropdown.setMinimumWidth(200)
        self.counter_dropdown.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.counter_dropdown.currentTextChanged.connect(self.on_counter_changed)
        self.layout.addWidget(self.counter_dropdown, alignment=Qt.AlignCenter)

        self.layout.addWidget(QLabel("Select Counter:"), alignment=Qt.AlignCenter)

        # Add button
        self.add_button = QPushButton("Add New Counter")
        self.add_button.clicked.connect(self.add_counter)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        # Counter row
        row = QHBoxLayout()
        self.minus_btn = QPushButton("-")
        self.minus_btn.setFont(QFont("Segoe UI", 40))
        self.minus_btn.clicked.connect(lambda: self.change_value(-1))
        row.addWidget(self.minus_btn)

        self.today_label = QLabel()
        self.today_label.setAlignment(Qt.AlignCenter)
        self.today_label.setFont(header_font)
        row.addWidget(self.today_label)

        self.plus_btn = QPushButton("+")
        self.plus_btn.setFont(QFont("Segoe UI", 40))
        self.plus_btn.clicked.connect(lambda: self.change_value(1))
        row.addWidget(self.plus_btn)

        self.layout.addLayout(row)

        # Month nav
        month_row = QHBoxLayout()
        month_row.setSpacing(10)

        self.prev_btn = QPushButton("←")
        self.prev_btn.setFixedSize(32, 32)
        self.prev_btn.setFont(QFont("Segoe UI", 14))
        self.prev_btn.clicked.connect(self.prev_month)

        self.month_label = QLabel()
        self.month_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.month_label.setAlignment(Qt.AlignCenter)

        self.next_btn = QPushButton("→")
        self.next_btn.setFixedSize(32, 32)
        self.next_btn.setFont(QFont("Segoe UI", 14))
        self.next_btn.clicked.connect(self.next_month)

        month_row.addStretch(1)
        month_row.addWidget(self.prev_btn)
        month_row.addSpacing(10)
        month_row.addWidget(self.month_label)
        month_row.addSpacing(10)
        month_row.addWidget(self.next_btn)
        month_row.addStretch(1)

        self.layout.addSpacing(15)
        self.layout.addLayout(month_row)

        self.layout.addWidget(QLabel("This Month's Activity:"), alignment=Qt.AlignCenter)

        # Calendar grid
        self.grid = QGridLayout()
        self.grid.setSpacing(8)
        self.grid_frame = QFrame()
        self.grid_frame.setLayout(self.grid)
        self.layout.addWidget(self.grid_frame, alignment=Qt.AlignCenter)

        # Remove button
        self.remove_btn = QPushButton("Remove Selected Counter")
        self.remove_btn.setStyleSheet("background-color: #8b0000; color: white; font-weight: bold; padding: 6px 12px;")
        self.remove_btn.clicked.connect(self.remove_counter)
        self.layout.addWidget(self.remove_btn, alignment=Qt.AlignCenter)

        # Dark/light toggle
        self.toggle_btn = QPushButton("Toggle Theme")
        self.toggle_btn.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.toggle_btn, alignment=Qt.AlignCenter)

        self.set_theme()
        self.apply_button_styles()

    def apply_button_styles(self):
        border = "white" if self.is_dark_mode else "black"
        bg = "#1f1f1f" if self.is_dark_mode else "#f0f0f0"
        text = "white" if self.is_dark_mode else "black"

        self.plus_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border};")
        self.minus_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border};")
        self.prev_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border};")
        self.next_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border};")
        self.add_button.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border}; padding: 6px 12px;")
        self.toggle_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border}; padding: 6px 12px;")

        self.plus_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border};")
        self.minus_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border};")
        self.prev_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border};")
        self.next_btn.setStyleSheet(f"background-color: {bg}; color: {text}; border: 1px solid {border};")


    def set_theme(self):
        dark = self.is_dark_mode
        pal = QPalette()
        if dark:
            pal.setColor(QPalette.Window, QColor("#000000"))
            pal.setColor(QPalette.WindowText, QColor("white"))
            pal.setColor(QPalette.Button, QColor("#1f1f1f"))
            pal.setColor(QPalette.ButtonText, QColor("white"))
        else:
            pal.setColor(QPalette.Window, QColor("#ffffff"))
            pal.setColor(QPalette.WindowText, QColor("#000000"))
            pal.setColor(QPalette.Button, QColor("#f0f0f0"))
            pal.setColor(QPalette.ButtonText, QColor("#000000"))
        self.setPalette(pal)

    def refresh_counter_menu(self):
        self.counter_dropdown.clear()
        self.counter_dropdown.addItems(data.keys())
        if data:
            self.selected_counter = next(iter(data))
            self.counter_dropdown.setCurrentText(self.selected_counter)

    def on_counter_changed(self, name):
        self.selected_counter = name
        self.update_today_label()
        self.draw_calendar()

    def update_today_label(self):
        today = date.today().isoformat()
        value = data.get(self.selected_counter, {}).get(today, 0)
        self.today_label.setText(f"Today: {value}")

    def change_value(self, delta):
        today = date.today().isoformat()
        if not self.selected_counter:
            return
        data.setdefault(self.selected_counter, {})
        data[self.selected_counter][today] = max(0, data[self.selected_counter].get(today, 0) + delta)
        self.update_today_label()
        self.draw_calendar()
        self.save_data()

    def draw_calendar(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.month_label.setText(self.current_date.strftime("%B %Y"))

        headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(headers):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(lbl, 0, col)

        first_day = self.current_date
        start_day_idx = first_day.weekday()
        num_days = monthrange(first_day.year, first_day.month)[1]

        row = 1
        col = (start_day_idx + 1) % 7

        for day_num in range(1, num_days + 1):
            d = date(first_day.year, first_day.month, day_num).isoformat()
            val = data.get(self.selected_counter, {}).get(d, 0)
            btn = QPushButton(str(day_num))
            if val == 0:
                btn.setStyleSheet("background-color: #3c3c3c; color: white;")
            elif val < 3:
                btn.setStyleSheet("background-color: #66c2a5; color: black;")
            elif val < 6:
                btn.setStyleSheet("background-color: #2ca25f; color: black;")
            else:
                btn.setStyleSheet("background-color: #006d2c; color: white;")

            btn.setToolTip(f"Count: {val}")
            self.grid.addWidget(btn, row, col)
            col += 1
            if col > 6:
                col = 0
                row += 1

    def add_counter(self):
        from PySide6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "New Counter", "Enter counter name:")
        if ok and name:
            if name not in data:
                data[name] = {}
                self.save_data()
                self.refresh_counter_menu()
            self.counter_dropdown.setCurrentText(name)

    def remove_counter(self):
        if self.selected_counter and self.selected_counter in data:
            confirm = QMessageBox.question(self, "Confirm", f"Delete '{self.selected_counter}' counter?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                del data[self.selected_counter]
                self.save_data()
                self.refresh_counter_menu()
                self.draw_calendar()

    def prev_month(self):
        self.current_date = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        self.draw_calendar()

    def next_month(self):
        year = self.current_date.year + (self.current_date.month // 12)
        month = (self.current_date.month % 12) + 1
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self.draw_calendar()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.set_theme()
        self.apply_button_styles()

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == '__main__':
    import ctypes
    myappid = 'com.aryan.tracker.dailycounter.v1'  # Any unique string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app = QApplication(sys.argv)
    window = CounterApp()

    # Set icon from extracted temp path (works inside .exe)
    ico_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), "Tracker_icon.ico")
    window.setWindowIcon(QIcon(ico_path))

    window.show()
    sys.exit(app.exec())

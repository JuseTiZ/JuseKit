# Study_record.py
# Author: Juse
# Description: The window of function 'Study record'.

from PyQt5.QtWidgets import QDialog, QHeaderView, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
import csv
import datetime
import time
import os
import re

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def replace_time(text, date, new_time):
    pattern = r'(' + date + r',)(\d{2}:\d{2}:\d{2})'
    replacement = r'\g<1>' + new_time
    result = re.sub(pattern, replacement, text)
    return result

class RecordsWindow(QDialog):
    def __init__(self, records, parent=None):
        super().__init__(parent)
        self.setWindowTitle("学习记录")
        self.setWindowIcon(QIcon("jusekit.ico"))
        self.init_ui(records)

    def init_ui(self, records):
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["日期", "学习时长"])
        self.table.setRowCount(len(records))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, (date, duration) in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(duration))

        self.layout.addWidget(self.table)

class LearningTimerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("学习计时器")
        self.setFixedSize(350, 200)
        self.setWindowIcon(QIcon("jusekit.ico"))

        self.time_elapsed = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

        self.init_ui()

        self.today = datetime.date.today().strftime("%Y-%m-%d")
        if os.path.exists("records.csv"):
            with open("records.csv", "r") as f:
                records = list(csv.reader(f))
                for record in records:
                    if record[0] == self.today:
                        self.time_elapsed = time_to_seconds(record[1])
                        ts = time.strftime("%H:%M:%S", time.gmtime(self.time_elapsed))
                        self.time_label.setText(ts)
                        break
                else:
                    self.time_elapsed = 0
        else:
            self.time_elapsed = 0

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.time_label = QLabel("00:00:00")
        self.layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            font-family: "Microsoft YaHei";
            font-size: 45px;
            font-weight: bold;
            color: #4a4a4a;
        """)

        self.start_button = QPushButton("开始学习")
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        self.pause_button = QPushButton("暂停学习")
        self.pause_button.clicked.connect(self.pause_timer)
        self.layout.addWidget(self.pause_button)

        self.records_button = QPushButton("学习记录")
        self.records_button.clicked.connect(self.show_records)
        self.layout.addWidget(self.records_button)
    def start_timer(self):
        self.timer.start(1000)  # 计时器以1秒（1000毫秒）的间隔触发

    def pause_timer(self):
        self.timer.stop()
        self.save_record()

    def update_time(self):
        self.time_elapsed += 1
        time_string = time.strftime("%H:%M:%S", time.gmtime(self.time_elapsed))
        self.time_label.setText(time_string)

    def save_record(self):

        time_str = time.strftime("%H:%M:%S", time.gmtime(self.time_elapsed))

        if os.path.exists("records.csv"):
            cfile = open('records.csv','r')
            content = cfile.read()
            if self.today in content:
                content = replace_time(content, self.today, time_str)
                with open("records.csv", 'w') as f:
                    f.write(content)
            else:
                with open("records.csv", "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([self.today, time_str])
        else:
            with open("records.csv", "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([self.today, time_str])

    def show_records(self):
        records = []
        try:
            with open("records.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    records.append(row)
        except FileNotFoundError:
            pass

        records_window = RecordsWindow(records, self)
        records_window.exec_()
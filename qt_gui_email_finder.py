from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTreeView, QLineEdit, QMainWindow, QMessageBox, QFileDialog, QCheckBox, QGridLayout, QDoubleSpinBox, QListWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import os

import re
import requests
import requests.exceptions
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import warnings
from bs4 import GuessedAtParserWarning, MarkupResemblesLocatorWarning
import time


class EmailFinderApp(QMainWindow):
    def __init__(self):
        super(EmailFinderApp, self).__init__()
        self.setWindowTitle("EmailFinder 1.0")
        self.resize(800, 300)

        main_window = QWidget()

        self.master_layout = QVBoxLayout()

        self.url_lbl = QLabel("Url:")
        self.url_fld = QLineEdit()

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.find_emails)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.testing)

        self.close_btn = QPushButton("Close")
        self.time_limit_chk = QCheckBox("Time Limit, sec: ")
        self.time_limit_num = QDoubleSpinBox()

        self.page_limit_chk = QCheckBox("Page Limit: ")
        self.page_limit_num = QDoubleSpinBox()

        # Creation of a TreeView

        self.output_list = QListWidget()
        self.output_list.updatesEnabled()

        self.master_layout = QGridLayout()

        self.master_layout.addWidget(self.url_lbl, 0, 0)
        self.master_layout.addWidget(self.url_fld, 0, 2)
        self.master_layout.addWidget(self.search_btn, 0, 3)
        self.master_layout.addWidget(self.stop_btn, 0, 4)
        self.master_layout.addWidget(self.close_btn, 0, 5)

        self.master_layout.addWidget(self.output_list, 1, 2, 3, 1)

        self.master_layout.addWidget(self.time_limit_chk, 1, 3)
        self.master_layout.addWidget(self.time_limit_num, 1, 4)

        self.master_layout.addWidget(self.page_limit_chk, 2, 3)
        self.master_layout.addWidget(self.page_limit_num, 2, 4)

        self.master_layout.setAlignment(Qt.AlignTop)

        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)

    def testing(self):
        self.output_list.clear()
        for i in range(10):
            time.sleep(1)
            self.output_list.addItem(str(i))
            self.output_list.commitData()

    def find_emails(self):
        warnings.filterwarnings('ignore', category=GuessedAtParserWarning)
        warnings.filterwarnings(
            'ignore', category=MarkupResemblesLocatorWarning)

        base_url = self.url_fld.text()
        print(base_url)

        urls = []
        emails = set()
        if base_url not in urls:
            urls.append(base_url)

        for next_url in urls:
            try:
                response = requests.get(next_url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue
            print(f"Crawling URL =================== {next_url} ")
            self.output_list.addItem(
                f"Crawling URL =================== {next_url} ")

            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all("a")
            new_emails = set(re.findall(
                r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))

            if len(new_emails) > 0:
                print(f"Found: {new_emails}")
                self.output_list.addItem(f"Found: {new_emails}")
                emails.update(new_emails)

            for link in links:
                if link.get("href"):

                    if ((next_url not in link.get("href")) & ("http" not in link.get("href")) & ("www" not in link.get("href"))):
                        page_url = base_url.strip(
                            "/") + "/" + link.get("href").strip("/")
                        if page_url not in urls:
                            urls.append(page_url)
                            print(f"Adding page # {len(urls)}: {page_url}")
                            self.output_list.addItem(
                                f"Adding page # {len(urls)}: {page_url}")
                            self.output_list.update()

                    elif (next_url in link.get("href")):
                        page_url = link.get("href")
                        if page_url not in urls:
                            urls.append(page_url)
                            print(
                                f"Adding: {page_url} Number Added: {len(urls)}")

                            self.output_list.addItem(
                                f"Adding: {page_url} Number Added: {len(urls)}")
                self.output_list.update()

        print(f"Total number of URLs:   {len(urls)}")
        print(f"Total number of Emails: {len(emails)}")

        self.output_list.addItem(f"Total number of URLs:   {len(urls)}")
        self.output_list.addItem(f"Total number of Emails: {len(emails)}")

        for email in emails:
            print(email)
            self.output_list.addItem(email)


if __name__ == "__main__":
    app = QApplication([])
    my_app = EmailFinderApp()
    my_app.show()
    app.exec_()
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTreeView, QLineEdit, QMainWindow, QMessageBox, QFileDialog, QCheckBox, QGridLayout, QDoubleSpinBox
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
        self.close_btn = QPushButton("Close")
        self.time_limit_chk = QCheckBox("Time Limit, sec: ")
        self.time_limit_num = QDoubleSpinBox()

        self.page_limit_chk = QCheckBox("Page Limit: ")
        self.page_limit_num = QDoubleSpinBox()

        # Creation of a TreeView
        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        self.master_layout = QGridLayout()

        self.master_layout.addWidget(self.url_lbl, 0, 0)
        self.master_layout.addWidget(self.url_fld, 0, 2)
        self.master_layout.addWidget(self.search_btn, 0, 3)
        self.master_layout.addWidget(self.stop_btn, 0, 4)
        self.master_layout.addWidget(self.close_btn, 0, 5)

        self.master_layout.addWidget(self.tree_view, 1, 2, 3, 1)

        self.master_layout.addWidget(self.time_limit_chk, 1, 3)
        self.master_layout.addWidget(self.time_limit_num, 1, 4)

        self.master_layout.addWidget(self.page_limit_chk, 2, 3)
        self.master_layout.addWidget(self.page_limit_num, 2, 4)

        self.master_layout.setAlignment(Qt.AlignTop)

        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)

    def find_emails(self):
        self.model.clear()
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
            self.model.appendRow(
                [QStandardItem(f"Crawling URL =================== {next_url} ")])
            self.tree_view.update()

            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all("a")
            new_emails = set(re.findall(
                r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))

            if len(new_emails) > 0:
                print(f"Found: {new_emails}")
                emails.update(new_emails)

            for link in links:
                if link.get("href"):

                    if ((next_url not in link.get("href")) & ("http" not in link.get("href")) & ("www" not in link.get("href"))):
                        page_url = base_url.strip(
                            "/") + "/" + link.get("href").strip("/")
                        if page_url not in urls:
                            urls.append(page_url)
                            print(f"Adding page # {len(urls)}: {page_url}")
                            self.model.appendRow(
                                [QStandardItem(f"Adding page # {len(urls)}: {page_url}")])
                            self.tree_view.update()

                    elif (next_url in link.get("href")):
                        page_url = link.get("href")
                        if page_url not in urls:
                            urls.append(page_url)
                            print(
                                f"Adding: {page_url} Number Added: {len(urls)}")
                            self.model.appendRow(
                                [QStandardItem(f"Adding: {page_url} Number Added: {len(urls)}")])
                            self.tree_view.update()

        print(f"Total number of URLs:   {len(urls)}")
        print(f"Total number of Emails: {len(emails)}")
        self.model.appendRow(
            [QStandardItem(f"Total number of URLs:   {len(urls)}")])
        self.model.appendRow(
            [QStandardItem(f"Total number of Emails: {len(emails)}")])
        self.tree_view.update()

        for email in emails:
            print(email)
            self.model.appendRow([QStandardItem(email)])


if __name__ == "__main__":
    app = QApplication([])
    my_app = EmailFinderApp()
    my_app.show()
    app.exec_()

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTreeView, QLineEdit, QMainWindow, QMessageBox, QFileDialog, QCheckBox, QGridLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import os


class EmailFinderApp(QMainWindow):
    def __init__(self):
        super(EmailFinderApp, self).__init__()
        self.setWindowTitle("EmailFinder 1.0")
        self.resize(800, 600)

        main_window = QWidget()

        self.master_layout = QVBoxLayout()

        self.url_lbl = QLabel("Url:")
        self.url_fld = QLineEdit()

        self.search_btn = QPushButton("Search")
        self.stop_btn = QPushButton("Stop")
        self.close_btn = QPushButton("Close")

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
        self.master_layout.addWidget(self.tree_view, 1, 1)

        self.master_layout.setAlignment(Qt.AlignTop)

        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)


if __name__ == "__main__":
    app = QApplication([])
    my_app = EmailFinderApp()
    my_app.show()
    app.exec_()

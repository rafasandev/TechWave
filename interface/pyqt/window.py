import sys

from terminal import Terminal
from modal import Modal
import graph

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter,
    QTextEdit,
    QLabel,
    QToolButton,
    QStyle,
    QPushButton,
)
from PyQt6.QtGui import QMouseEvent, QPalette
from PyQt6.QtCore import Qt, QSize, QEvent
from PyQt6.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tech Wave")
        self.setMinimumSize(920, 720)

        self.terminal_widget = Terminal()

        self.graph_html = graph.generate_graph_html()
        self.graph_html = self.graph_html.replace(
            "<body>", "<body style='margin: -10px -2px 15px -2px; overflow: hidden;'>"
        )

        self.graph_view = QWebEngineView()

        self.graph_view.setHtml(self.graph_html)

        self.terminal_widget.setMinimumWidth(150)

        self.splitter = QSplitter()
        self.splitter.addWidget(self.terminal_widget)
        self.splitter.addWidget(self.graph_view)
        self.splitter.setStyleSheet(
            """
            background-color: #5C5C5C;
        """
        )

        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.splitter)

        self.floating_window = Modal(self)

        # self.button = QPushButton("Abrir modal", self)
        # self.button.clicked.connect(self.open_modal)

        # self.central_layout.addWidget(self.button)

        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_layout)

        self.setCentralWidget(self.central_widget)

    def open_modal(self):
        self.floating_window.move(300, 200)
        self.floating_window.show()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

import sys

from terminal import Terminal
import graph
import sqlite3

from compiler.graph_scene import GraphScene

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
)
from PyQt6.QtGui import QMouseEvent, QPalette
from PyQt6.QtCore import Qt, QSize, QEvent
from PyQt6.QtWebEngineWidgets import QWebEngineView

conn = sqlite3.connect("graph.db")


class MainWindow(QMainWindow):

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

        self.setWindowTitle("Tech Wave")
        self.setMinimumSize(920, 720)

        self.terminal_widget = Terminal()
        self.terminal_widget.graph_updated.connect(self.update_graph)

        graph.get_graph_db()

        self.graph_html = graph.generate_regular_graph()
        self.graph_html = self.graph_html.replace(
            "<body>", "<body style='margin: -10px -2px 15px -2px; overflow: hidden;'>"
        )

        self.graph_view = QWebEngineView()
        self.graph_view.setHtml(self.graph_html)

        self.splitter = QSplitter()
        self.splitter.addWidget(self.terminal_widget)
        self.splitter.addWidget(self.graph_view)
        self.splitter.setStyleSheet(
            """
            background-color: #272E25;
        """
        )

        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.splitter)

        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0, 0, 0, 0)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_layout)

        self.setCentralWidget(self.central_widget)

        self.showMaximized()

    def update_graph(self):

        format = self.terminal_widget.format_graph

        if format == "regular":
            self.graph_html = graph.generate_regular_graph()
        elif format == "communities":
            self.graph_html = graph.generate_community_graph()

        self.graph_html = self.graph_html.replace(
            "<body>", "<body style='margin: -10px -2px 15px -2px; overflow: hidden;'>"
        )
        self.graph_view.setHtml(self.graph_html)


app = QApplication(sys.argv)

window = MainWindow(conn)
window.show()

app.exec()

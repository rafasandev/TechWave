import sys
import os
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLineEdit, QGraphicsView
from PyQt6.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from compiler.main import *
from compiler.graph_scene import *


class Terminal(QWidget):

    graph_updated = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.terminal = QTextEdit(self)
        self.terminal.setReadOnly(True)
        self.terminal.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.terminal.setMinimumWidth(200)

        self.terminal.setStyleSheet(
            """
            background-color: #121311; 
            padding: 5px; 
            color: #ffffff;
            border: none;
            font-weight: bold;
            font-size: 14px;
        """
        )

        self.input = QLineEdit(self)
        self.input.returnPressed.connect(self.process_command)
        self.input.setStyleSheet(
            """
            background-color: #485544; 
            padding: 5px; 
            color: #ffffff;
            border: none;
            border-top: 2px solid #444444;
            font-weight: bold;
            font-size: 14px;
        """
        )

        self.terminal_layout = QVBoxLayout()
        self.terminal_layout.addWidget(self.terminal)
        self.terminal_layout.addWidget(self.input)

        self.terminal_layout.setSpacing(0)
        self.terminal_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.terminal_layout)

    def process_command(self):
        command = self.input.text()

        output = f"> {command}\n"
        self.terminal.append(output)
        self.terminal.verticalScrollBar().setValue(
            self.terminal.verticalScrollBar().maximum()
        )

        self.input.clear()

        graph_view = GraphScene()

        if command == "cls":
            self.terminal.clear()
            response = ""

        elif command == "list":
            response = ""

        else:
            response = process_command(command, graph_view)

        self.terminal.append(response)

        self.terminal.verticalScrollBar().setValue(
            self.terminal.verticalScrollBar().maximum()
        )

        self.graph_updated.emit()

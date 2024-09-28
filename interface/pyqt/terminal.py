import sys
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt


class Terminal(QWidget):

    def __init__(self):
        super().__init__()

        self.terminal = QTextEdit()
        self.terminal.setStyleSheet(
            """
            background-color: #272E25; 
            padding: 5px; 
            color: #ffffff;
            border: none;
            font-weight: bold;
            font-size: 14px;
        """
        )

        self.terminal.textChanged.connect(self.getTerminalContent)

        self.terminal_layout = QVBoxLayout()
        self.terminal_layout.addWidget(self.terminal)

        self.terminal_layout.setSpacing(0)
        self.terminal_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.terminal_layout)

    def getTerminalContent(self):
        print(self.terminal.toHtml())
        print(self.terminal.toHtml().index("<p"))

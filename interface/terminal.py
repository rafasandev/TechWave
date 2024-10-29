# from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLineEdit

# from PyQt6.QtCore import Qt, QEvent


class Terminal(QWidget):

    def __init__(self):
        super().__init__()

        self.terminal = QTextEdit(self)
        self.terminal.setReadOnly(True)
        self.terminal.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

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
        self.input.clear()
        self.terminal.verticalScrollBar().setValue(
            self.terminal.verticalScrollBar().maximum()
        )

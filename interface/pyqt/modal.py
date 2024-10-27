import sys
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QDialog, QLabel, QApplication
from PyQt6.QtCore import QPoint

class Modal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Modal")
        self.setFixedSize(300,200)

        self.label = QLabel("Modal Flutuante")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
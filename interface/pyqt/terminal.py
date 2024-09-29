import sys
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import Qt

class Terminal(QTextEdit):
    
    def __init__(self):
        super().__init__()

        self.terminal = QTextEdit()
        self.terminal.setStyleSheet("""
            background-color: #272E25; 
            padding: 5px; 
            color: #ffffff;
            border: none;
            font-size: 14px;
            font-weight: bold;
        """)

        self.terminal_layout = QVBoxLayout()
        self.terminal_layout.addWidget(self.terminal)
        
        self.terminal_layout.setSpacing(0)
        self.terminal_layout.setContentsMargins(0,0,0,0)

        self.setLayout(self.terminal_layout)

        self.setReadOnly(False)
        self.prompt_pos = 0  # Posição do prompt

        # Definir um estilo básico de terminal
        self.append("Welcome to the terminal!")
        self.append(">>> ")  # Prompt inicial
        self.prompt_pos = self.textCursor().position()  # Posição do prompt após o ">>>"

        # Sinal de captura de teclas
        self.textChanged.connect(self._lock_text_above_prompt)

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        key = event.key()

        # Se o usuário pressionar Backspace no prompt, impedir a exclusão do texto anterior
        if key == Qt.Key.Key_Backspace and cursor.position() <= self.prompt_pos:
            return

        # Capturar a tecla Enter para processar o comando
        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self.process_command()
            return

        # Permitir as demais teclas normais
        super().keyPressEvent(event)

    def process_command(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)

        # Capturar o comando inserido
        user_input = self.toPlainText()[self.prompt_pos:]
        self.append(f"Processing command: {user_input.strip()}")

        # Adicionar um novo prompt
        self.append(">>> ")
        self.prompt_pos = self.textCursor().position()

    def _lock_text_above_prompt(self):
        """ Impedir modificações acima do prompt atual. """
        cursor = self.textCursor()
        if cursor.position() < self.prompt_pos:
            cursor.setPosition(self.prompt_pos)
            self.setTextCursor(cursor)
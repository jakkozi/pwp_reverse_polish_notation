from PyQt6.QtWidgets import (QWidget, QGridLayout, 
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt6.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Calculator")
        width, height = 300, 450
        self.setFixedSize(width, height) # Starting size
        # Explicitly force the range to match
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

        # 1. Main Layout (Vertical)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 2. Display (QLineEdit)
        self.display = QLineEdit()
        # self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)  # User must use buttons
        self.main_layout.addWidget(self.display)

        # 3. Keypad (QGridLayout)
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.create_buttons()

    def create_buttons(self):
        # Clear Button: Row 0, Col 0, spans 1 row, spans 2 column
        btn_clear = QPushButton('C')
        btn_clear.clicked.connect(self.clear_display)
        self.grid_layout.addWidget(btn_clear, 0, 0, 1, 2)

        # Backspace Button: Row 0, Col 2, spans 1 row, spans 2 columns
        btn_back = QPushButton('<-')
        btn_back.clicked.connect(self.backspace)
        self.grid_layout.addWidget(btn_back, 0, 2, 1, 2)

        # Define button labels and their positions (row, col)
        buttons = {
            '7': (1, 0), '8': (1, 1), '9': (1, 2), '/': (1, 3),
            '4': (2, 0), '5': (2, 1), '6': (2, 2), '*': (2, 3),
            '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
            ',': (4, 0), '0': (4, 1), '=': (4, 2), '+': (4, 3),
        }

        for text, pos in buttons.items():
            btn = QPushButton(text)
            
            # Connect the button's clicked signal
            if text == '=':
                btn.clicked.connect(self.calculate_result)
            elif text == 'C':
                btn.clicked.connect(self.clear_display)
            else:
                # Use lambda to pass the button text to the function
                btn.clicked.connect(lambda checked, t=text: self.append_text(t))
                
            self.grid_layout.addWidget(btn, *pos)

    def backspace(self):
        current_text = self.display.text()
        self.display.setText(current_text[:-1])

    def append_text(self, text):
        self.display.setText(self.display.text() + text)

    def clear_display(self):
        self.display.clear()

    def calculate_result(self):
        try:
            # eval() is the simplest way to solve math strings
            result = eval(self.display.text())
            self.display.setText(str(result))
        except Exception:
            self.display.setText("Error")
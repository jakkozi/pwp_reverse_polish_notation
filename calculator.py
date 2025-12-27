from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtCore import QTimer
from functools import wraps


def sync_ui(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # 1. Execute the actual logic (e.g., appending to the array)
        result = method(self, *args, **kwargs)

        # 2. Trigger the UI update automatically
        self.sync_display()

        return result

    return wrapper


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # Data storage
        self.expression = []
        self.currently_inputed_number = []

        self.setWindowTitle("PyQt6 Calculator")
        width, height = 300, 450
        self.setFixedSize(width, height)  # Starting size
        # Explicitly force the range to match
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

        # 1. Main Layout (Vertical)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 2. Display (QLineEdit)
        self.display = QLineEdit()
        self.display.setReadOnly(True)  # User must use buttons
        self.main_layout.addWidget(self.display)

        # 3. Flashing indicator timer
        self.flash_timer = QTimer(self)
        self.flash_on = False
        self.flash_timer.timeout.connect(lambda: self.toggle_flash_state())
        self.display.setProperty("flashing", self.flash_on)

        # 4. Keypad (QGridLayout)
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.create_buttons()

    def create_buttons(self):
        # Clear Button: Row 0, Col 0, spans 1 row, spans 2 column
        btn_clear = QPushButton("C")
        btn_clear.clicked.connect(lambda: self.clear_display())
        self.grid_layout.addWidget(btn_clear, 0, 0, 1, 2)

        # Backspace Button: Row 0, Col 2, spans 1 row, spans 2 columns
        btn_back = QPushButton("<-")
        btn_back.clicked.connect(lambda: self.backspace())
        self.grid_layout.addWidget(btn_back, 0, 2, 1, 2)

        # Define button labels and their positions (row, col)
        buttons = {
            "7": (1, 0),
            "8": (1, 1),
            "9": (1, 2),
            "/": (1, 3),
            "4": (2, 0),
            "5": (2, 1),
            "6": (2, 2),
            "*": (2, 3),
            "1": (3, 0),
            "2": (3, 1),
            "3": (3, 2),
            "-": (3, 3),
            ",": (4, 0),
            "0": (4, 1),
            "=": (4, 2),
            "+": (4, 3),
        }

        for text, pos in buttons.items():
            btn = QPushButton(text)

            # Connect the button's clicked signal
            if text == "=":
                btn.clicked.connect(lambda: self.calculate_result())
            else:
                # Use lambda to pass the button text to the function
                btn.clicked.connect(lambda checked, t=text: self.append_text(t))

            self.grid_layout.addWidget(btn, *pos)

    def sync_display(self):
        display_text = "".join(self.expression)
        current_num = "".join(self.currently_inputed_number)

        if len(self.currently_inputed_number) > 0:
            if not self.flash_timer.isActive():
                self.flash_timer.start(500)  # Flash every 500ms

            indicator = "|" if self.flash_on else ""
            display_text += current_num + indicator
        else:
            self.flash_timer.stop()
            display_text += current_num

        self.display.setText(display_text)

    @sync_ui
    def toggle_flash_state(self):
        self.flash_on = not self.flash_on
        self.display.setProperty("flashing", self.flash_on)

        # Re-apply qss rules
        self.display.style().unpolish(self.display)
        self.display.style().polish(self.display)

    @sync_ui
    def backspace(self):
        if len(self.currently_inputed_number) > 0:
            self.currently_inputed_number.pop()
        elif len(self.expression) > 0:
            self.expression.pop()

    @sync_ui
    def append_text(self, text):
        if text in [",", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            if text == "," and "," not in self.currently_inputed_number:
                if len(self.currently_inputed_number) == 0:
                    self.currently_inputed_number.append(["0", ","])
                else:
                    self.currently_inputed_number.append(",")
            else:
                self.currently_inputed_number.append(text)
        else:
            self.expression.append(text)

    @sync_ui
    def clear_display(self):
        self.expression.clear()

    @sync_ui
    def calculate_result(self):
        try:
            # eval() is the simplest way to solve math strings
            result = eval("".join(self.expression))
            self.expression = [result]
        except Exception:
            self.expression = ["Error"]

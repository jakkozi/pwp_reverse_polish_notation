from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt6.QtCore import QTimer
from functools import wraps
from calculator_item import Operator, CalculatorItem, isNumber
from typing import List
import rpn_calculator as RPNCalculator


def sync_ui(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # 1. Execute the actual logic (e.g., appending to the array)
        result = method(self, *args, **kwargs)

        # 2. Trigger the UI update automatically
        self._sync_display()

        return result

    return wrapper


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # Data storage
        self.expression: List[CalculatorItem] = []
        self.currently_inputed_number: List[str] = []

        self.setWindowTitle("PyQt6 Calculator")
        width, height = 400, 450
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
        self.flash_timer.timeout.connect(lambda: self._toggle_flash_state())
        self.display.setProperty("flashing", self.flash_on)

        # 4. Keypad (QGridLayout)
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self._create_buttons()

    def _create_buttons(self):
        # Clear Button: Row 0, Col 0, spans 1 row, spans 2 column
        btn_clear = QPushButton("C")
        btn_clear.clicked.connect(lambda: self._clear_display())
        self.grid_layout.addWidget(btn_clear, 0, 0, 1, 2)

        # Backspace Button: Row 0, Col 2, spans 1 row, spans 2 columns
        btn_back = QPushButton("<-")
        btn_back.clicked.connect(lambda: self._backspace())
        btn_back.setShortcut("Backspace")
        self.grid_layout.addWidget(btn_back, 0, 2, 1, 3)

        # Enter Button: Row 1, Col 4, spans 3 row, spans 1 columns
        btn_back = QPushButton("↵")
        btn_back.clicked.connect(lambda: self._enter())
        btn_back.setShortcut("Enter")
        self.grid_layout.addWidget(btn_back, 1, 4, 3, 1)

        # "Label": (positio, value, shortcut)
        buttons = {
            "7": ((1, 0), 7, '7'),
            "8": ((1, 1), 8, '8'),
            "9": ((1, 2), 9, '9'),
            "/": ((1, 3), Operator.DIV, '/'),
            "4": ((2, 0), 4, '4'),
            "5": ((2, 1), 5, '5'),
            "6": ((2, 2), 6, '6'),
            "*": ((2, 3), Operator.MUL, '*'),
            "1": ((3, 0), 1, '1'),
            "2": ((3, 1), 2, '2'),
            "3": ((3, 2), 3, '3'),
            "-": ((3, 3), Operator.SUB, '-'),
            ".": ((4, 0), Operator.DOT, ','),
            "0": ((4, 1), 0, '0'),
            "+/-": ((4, 2), Operator.NEG, 'Alt+-'),
            "+": ((4, 3), Operator.ADD, '+'),
            "=": ((4, 4), Operator.EQU, "Alt+Enter"),
        }

        for text, (pos, val, shortcut) in buttons.items():
            btn = QPushButton(text)
            btn.setShortcut(shortcut)

            match val:
                case Operator.EQU:
                    btn.clicked.connect(lambda: self._calculate_result())
                case _:
                    btn.clicked.connect(lambda _, v=val: self._append_text(v))

            self.grid_layout.addWidget(btn, *pos)

    def _sync_display(self):
        display_text = " ".join(map(str, self.expression))
        current_num = "".join(self.currently_inputed_number)

        if len(self.currently_inputed_number) > 0:
            if not self.flash_timer.isActive():
                self.flash_timer.start(500)  # Flash every 500ms

            indicator = "|" if self.flash_on else " "
            display_text += " " + current_num + indicator
        else:
            self.flash_timer.stop()
            display_text += current_num

        self.display.setText(display_text)

    @sync_ui
    def _toggle_flash_state(self):
        self.flash_on = not self.flash_on
        self.display.setProperty("flashing", self.flash_on)

    @sync_ui
    def _backspace(self):
        if len(self.currently_inputed_number) > 0:
            self.currently_inputed_number.pop()
            if len(self.currently_inputed_number) == 2 and self.currently_inputed_number[0] == '-' and self.currently_inputed_number[1] == '0':
                self.currently_inputed_number=['0']
        elif len(self.expression) > 0:
            lastValue = self.expression.pop()

            if isNumber(lastValue):
                self.currently_inputed_number = list(str(lastValue))
                self.currently_inputed_number.pop()

    @sync_ui
    def _append_text(self, val: CalculatorItem):
        match val:
            case 0:
                if not (
                    len(self.currently_inputed_number) == 1
                    and self.currently_inputed_number[0] == "0"
                ):
                    self.currently_inputed_number.append(str(val))
            case float(val) | int(val):
                if len(self.currently_inputed_number) == 1 and self.currently_inputed_number[0] == "0":
                    self.currently_inputed_number[0] = str(val)
                else:
                    self.currently_inputed_number.append(str(val))
            case Operator.NEG:
                if len(self.currently_inputed_number) > 0:
                    firstCharacter = self.currently_inputed_number[0]
                    if firstCharacter == '-':
                        self.currently_inputed_number.pop(0)
                    elif firstCharacter != '0' or firstCharacter == '0' and len(self.currently_inputed_number) > 1:
                        self.currently_inputed_number.insert(0, '-')

            case Operator.DOT:
                if "." not in self.currently_inputed_number:
                    if len(self.currently_inputed_number) == 0:
                        self.currently_inputed_number.append("0")
                        self.currently_inputed_number.append(".")
                    else:
                        self.currently_inputed_number.append(".")
            case _:
                self._enter()
                self.expression.append(val)

    @sync_ui
    def _enter(self):
        if len(self.currently_inputed_number) > 0:

            if "." in self.currently_inputed_number:
                # Remove trailing zeros
                while (
                    self.currently_inputed_number
                    and self.currently_inputed_number[-1] == "0"
                ):
                    self.currently_inputed_number.pop()

                # Remove unused dot
                if self.currently_inputed_number[-1] == ".":
                    self.currently_inputed_number.pop()

            number_str = "".join(self.currently_inputed_number)
            self.currently_inputed_number.clear()
            self.expression.append(
                float(number_str) if "." in number_str else int(number_str)
            )

    @sync_ui
    def _clear_display(self):
        self.currently_inputed_number.clear()
        self.expression.clear()

    @sync_ui
    def _calculate_result(self):
        self._enter()
        try:
            result = RPNCalculator.calculate(self.expression)
            if result.is_integer():
                result = int(result)
            self.expression = [str(result)]
        except Exception as e:
            self.expression = [e]
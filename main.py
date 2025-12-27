import sys
from PyQt6.QtWidgets import QApplication

from calculator import Calculator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("style.qss", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Warning: style.qss not found. Running with default styles.")

    calc = Calculator()
    calc.show()
    sys.exit(app.exec())

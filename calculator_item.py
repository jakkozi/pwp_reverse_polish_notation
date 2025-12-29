from enum import Enum
from typing import Union
from dataclasses import dataclass

class Operator(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    NEG = "+/-"
    EQU = "="
    DOT = "."

    def __str__(self) -> str:
        return self.value

CalculatorItem = Union[Operator, float, int]
from enum import Enum
from typing import Union

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

def isNumber(a):
    return isinstance(a, (float, int))
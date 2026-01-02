from typing import List
from calculator_item import CalculatorItem, Operator, isNumber

def calculate(input: List[CalculatorItem]):
    stack: List[float | int] = []
    for item in input:
        if isNumber(item):
            stack.append(item)
        elif len(stack) >= 2:
            b = stack.pop()
            a = stack.pop()
            result = _apply_operation(a, b, item)
            stack.append(result)
        else:
            raise ArithmeticError("Invalid equation")
    if len(stack) != 1:
        raise ArithmeticError("Invalid equation")
    result = stack[-1]
    return result

def _apply_operation(a: float | int, b: float | int, operator: Operator):
    # if not(isNumber(a) and isNumber(b)):
    #     raise TypeError(f"One of the operands is not a number: {a}, {b}")
    # if not isinstance(operator, Operator):
    #     raise TypeError(f"One of the supplied operators is not an operator: {operator}")
    match operator:
        case Operator.ADD:
            return a + b
        case Operator.SUB:
            return a - b
        case Operator.MUL:
            return a * b
        case Operator.DIV:
            if(b == 0):
                raise ZeroDivisionError("Can't divide by zero")
            return a / b
        case _:
            raise ValueError(f"Unrecognized operator: {operator}")

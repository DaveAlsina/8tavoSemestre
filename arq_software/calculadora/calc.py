import random

class Calculator:

    def __init__(self) -> None:
        pass

    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b
    
    @staticmethod
    def sub(a: int, b: int) -> int:
        return a - b
    
    @staticmethod
    def mul(a: int, b: int) -> int:
        return a * b

    @staticmethod
    def div(a: int, b: int) -> float:
        return a / b

    @staticmethod
    def idiv(a: int, b: int) -> int:
        return a // b

    @staticmethod
    def mod(a: int, b: int) -> int:
        return a % b
    
    @staticmethod
    def pow(a: int, b: int) -> int: 
        return a ** b

    def __str__(self) -> str:
        return f"Calculator class instance id: {id(self)}"


if __name__ == "__main__":

    #test operations for random numbers a and b
    a = random.randint(1, 100)
    b = random.randint(1, 100)

    print(f"a = {a}, b = {b}")

    print(f"{a} + {b} = {Calculator.add(a, b)}")
    print(f"{a} - {b} = {Calculator.sub(a, b)}")
    print(f"{a} * {b} = {Calculator.mul(a, b)}")
    print(f"{a} / {b} = {Calculator.div(a, b)}")
    print(f"{a} // {b} = {Calculator.idiv(a, b)}")
    print(f"{a} % {b} = {Calculator.mod(a, b)}")
    print(f"{a} ** {b} = {Calculator.pow(a, b)}")


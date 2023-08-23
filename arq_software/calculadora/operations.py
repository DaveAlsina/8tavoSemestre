from abc import ABC, abstractmethod

class Operation(ABC):
    def __init__(self, name = 'Operation') -> None:
        self.name = name

    @staticmethod
    def execute(a, b):
        """
        This method should be implemented in the child classes.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    

class Add(Operation):
    
    def __init__(self) -> None:
        super().__init__(name = 'Addition')

    @staticmethod
    def execute(a, b):
        return a + b


class Subtract(Operation):
    def __init__(self) -> None:
        super().__init__(name = 'Subtraction')

    @staticmethod
    def execute(a, b):
        return a - b

class Multiply(Operation):
    def __init__(self) -> None:
        super().__init__(name = 'Multiplication')

    @staticmethod
    def execute(a, b):
        return a * b

class Pow(Operation):
    def __init__(self) -> None:
        super().__init__(name = 'Power')

    @staticmethod
    def execute(a, b):
        return a ** b

class Divide(Operation):
    def __init__(self) -> None:
        super().__init__(name = 'Division')

    @staticmethod
    def execute(a, b):
        if b == 0:
            return float("inf")
        return a / b

class IntegerDivide(Operation):
    def __init__(self) -> None:
        super().__init__(name = 'Integer Division')

    @staticmethod
    def execute(a, b):
        if b == 0:
            return float("inf")
        if (a < 0) and (b > 0):
            return -(abs(a) // b)
        if (a > 0) and (b < 0):
            return -(a // abs(b))
        return a // b


class Mod(Operation):
    def __init__(self) -> None:
        super().__init__(name = 'Module')

    @staticmethod
    def execute(a, b):
        if b == 0:
            return float("inf")
        return a % b
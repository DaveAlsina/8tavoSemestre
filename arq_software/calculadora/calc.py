import random
from operations import Operation, Add, Subtract, Multiply, Divide, IntegerDivide, Mod, Pow

class Calculator:

    def __init__(self) -> None:
        """
        This class is a wrapper for the operations classes.    
        """
        self.operations = {0: Add(),
                           1: Subtract(),
                           2: Multiply(),
                           3: Divide(),
                           4: IntegerDivide(),
                           5: Mod(),
                           6: Pow()}

    def execute(self, op: Operation, a: int, b: int) -> float:
        """
        Executes the operation op with operands a and b.
        """
        return op.execute(a, b)

    def add(self, a: int, b: int) -> int:
        return self.execute(self.operations[0], a, b)
    
    def sub(self, a: int, b: int) -> int:
        return self.operations[1].execute(a, b)
    
    def mul(self, a: int, b: int) -> int:
        return self.execute(self.operations[1], a, b)

    def div(self, a: int, b: int) -> float:
        return self.execute(self.operations[2], a, b)

    def idiv(self, a: int, b: int) -> float:
        return self.execute(self.operations[3], a, b)

    def mod(self, a: int, b: int) -> int:
        return self.execute(self.operations[4], a, b)
    
    def pow(self, a: int, b: int) -> int: 
        return self.execute(self.operations[5], a, b)

    def __str__(self) -> str:
        return f"Calculator class instance id: {id(self)}"


if __name__ == "__main__":

    #set random seed 
    random.seed(2)

    #test operations for random numbers a and b
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    print(f"a = {a}, b = {b}")

    c = Calculator()

    print(f"{a} + {b} = {c.add(a, b)}")
    print(f"{a} - {b} = {c.sub(a, b)}")
    print(f"{a} * {b} = {c.mul(a, b)}")
    print(f"{a} / {b} = {c.div(a, b)}")
    print(f"{a} // {b} = {c.idiv(a, b)}")
    print(f"{a} % {b} = {c.mod(a, b)}")
    print(f"{a} ** {b} = {c.pow(a, b)}")
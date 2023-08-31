from typing import Union
from operation_manager import OperationManager

class Calculator:

    def __init__(self) -> None:
        """
        This class is a wrapper for the operations classes.    
        """
        self.operation_manager = OperationManager()

    def execute(self, operation_idx: int, a: int, b: int) -> Union[float , None]:
        """
        Executes the operation op with operands a and b.
        """
        operation = self.operation_manager.get_operation(operation_idx)

        if operation is None:
            return None
        else:
            return operation.execute(a, b)

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
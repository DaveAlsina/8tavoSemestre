from typing import Union
from operations import Operation, Add, Subtract, Multiply, Divide, IntegerDivide, Mod, Pow

class OperationManager:
    
    def __init__(self):

        self.operations = {0: Add(),
                           1: Subtract(),
                           2: Multiply(),
                           3: Divide(),
                           4: IntegerDivide(),
                           5: Mod(),
                           6: Pow()}

    def get_operation(self, index: int) -> Union[Operation, None]:
         return self.operations.get(index, None)

    def show_operations(self):
        for i, op in self.operations.items():
            print(f"{i}) {op}")
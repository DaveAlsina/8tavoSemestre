
from calc import Calculator

class Display:

    def __init__(self) -> None:
        self.c = Calculator()


    def take_input(self):
        self.a = int(input("Enter the first number: "))
        self.b = int(input("Enter the second number: "))

    def display_operations_menu(self) -> int:
        for i, op in self.c.operations.items():
            print(f"{i}) {op}")

        return int(input("Enter the operation number: "))

    def display_result(self, result):
        print(f"Result: {result}")
    

    def loop(self):

        while True:

            self.take_input()
            op = self.display_operations_menu()

            #gets the operation from the calculator, operations dict, if not found, returns None
            operation = self.c.operations.get(op, None)

            if operation is None:
                print("Invalid operation")
                continue
            
            result = operation.execute(self.a, self.b)
            self.display_result(result)

            if input("Do you want to continue? (y/n) ") == "n":
                break


if __name__ == "__main__":
    d = Display()
    d.loop()

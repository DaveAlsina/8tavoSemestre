from calc import Calculator

class Display:

    def __init__(self) -> None:
        self.c = Calculator()


    def take_input(self):
        self.a = int(input("Enter the first number: "))
        self.b = int(input("Enter the second number: "))

    def display_operations_menu(self) -> int:
        self.c.operation_manager.show_operations()
        return int(input("Enter the operation number: "))

    def display_result(self, result):
        print(f"Result: {result}")
    

    def loop(self):

        while True:

            self.take_input()
            op = self.display_operations_menu()

            #executes the operation, if it is valid gives the result, result is None
            result = self.c.execute(op, self.a, self.b)

            if result is None:
                print("Invalid operation")
                continue
            
            self.display_result(result)

            if input("Do you want to continue? (y/n) ") == "n":
                break


if __name__ == "__main__":
    d = Display()
    d.loop()

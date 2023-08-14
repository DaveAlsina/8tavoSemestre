class Vehicle:

    number_of_vehicles = 0

    def __init__(self, npassengers: int = 1) -> None:

        self.number_of_passengers = npassengers
        self.is_stopped = True

        # Increment the number of vehicles
        Vehicle.number_of_vehicles += 1
    
    def start_engine(self):
        self.is_stopped = False

    def __str__(self) -> str:
        return f"One Vehicle out of {Vehicle.number_of_vehicles} with {self.number_of_passengers} passengers."

if __name__ == "__main__":

    car = Vehicle(5)
    car.start_engine()

    print(car)

    bus = Vehicle(20)
    bus.start_engine()
    
    print(bus)
    
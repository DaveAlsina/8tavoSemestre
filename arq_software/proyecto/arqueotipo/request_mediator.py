import db_adapter
import data_validation

class RequestMediator():

    def __init__(self) -> None:
        print("RequestMediator: Inicializando...")
        self.adapter = db_adapter.DatabaseAdapter()
        self.data_validator = data_validation.DataValidator()

    def log_in(self, user: str, password: str):
        print(f"RequestMediator: log_in user: {user}, password: {password}")
        self.data_validator.validate_user(user, password)
        self.adapter.create_user(user, password)

    def create_user(self, user: str, password: str):
        print(f"RequestMediator: create_user user: {user}, password: {password}")
        self.data_validator.validate_user(user, password)
        self.adapter.create_user(user, password)

    def create_zone(self, zone: dict):
        print(f"RequestMediator: create_zone zone: {zone}")
        self.data_validator.validate_zone(zone)
        self.adapter.create_zone(zone)

    def add_measurement(self, measurement: dict):
        print(f"RequestMediator: add_measurement measurement: {measurement}")
        self.data_validator.validate_measurement(measurement)
        self.adapter.add_measurement(measurement)
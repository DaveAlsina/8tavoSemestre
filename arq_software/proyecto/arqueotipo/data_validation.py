
class DataValidator():

    def __init__(self) -> None:
        print("DataValidator: Inicializando...")

    def validate_user(self, user: str, password: str):
        print(f"DataValidator: validate_user user: {user}, password: {password}")

    def validate_zone(self, zone: dict):
        print(f"DataValidator: validate_zone zone: {zone}")

    def validate_measurement(self, measurement: dict):
        print(f"DataValidator: validate_measurement measurement: {measurement}")
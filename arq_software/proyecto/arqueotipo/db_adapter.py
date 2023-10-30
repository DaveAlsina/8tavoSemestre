from abc import ABC, abstractmethod

class DatabaseClient(ABC):

    @abstractmethod
    def create_user(self, user: str, password: str):
        pass
    
    @abstractmethod
    def create_zone(self, zone: dict):
        pass

    @abstractmethod
    def add_measurement(self, measurement: dict):
        pass

class DatabaseAdapter(DatabaseClient):

    def __init__(self) -> None:
        print("Database adapter: Inicializando...")

    def create_user(self, user: str, password: str):
        print(f"Database adapter: Creating user {user} with password {password}")

    def create_zone(self, zone: dict):
        print(f"Database adapter: Creating zone {zone}")

    def add_measurement(self, measurement: dict):
        print(f"Database adapter: Adding measurement {measurement}")
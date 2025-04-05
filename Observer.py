from abc import abstractmethod
from typing import Protocol

# abstract observer class for the observer pattern
class PlantObserver(Protocol):
    @abstractmethod
    def on_plant_placed(self, row: int, col: int, plant_name: str) -> None:
        pass
    
    @abstractmethod
    def on_plant_removed(self, row: int, col: int, plant_name: str) -> None:
        pass
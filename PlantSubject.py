from abc import abstractmethod, ABC
from .plantobserver import PlantObserver

# abstract subject class for the observer pattern
class PlantSubject(ABC):
    @abstractmethod
    def attach(self, observer: PlantObserver):
        pass

    @abstractmethod
    def notify_plant_placed(self, row: int, col: int, plant_name: str):
        pass

    @abstractmethod
    def notify_plant_removed(self, row: int, col: int, plant_name: str):
        pass
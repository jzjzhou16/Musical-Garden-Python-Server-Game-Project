from abc import abstractmethod, ABC
from .plant_observer import PlantObserver

# abstract subject class for the observer pattern
class PlantSubject(ABC):
    """
    Abstract class representing the subject in the observer pattern.
    It defines the methods for attaching observers and notifying them of changes.
    Parameters:
        observers (list[PlantObserver]): List of observers to be notified
    """
    @abstractmethod
    def attach(self, observer: PlantObserver):
        """
        Attach an observer to the subject.

        Preconditions:
            - The observer must be an instance of PlantObserver

        Parameters:
            observer (PlantObserver): The observer to attach
        """
        pass

    @abstractmethod
    def notify_plant_placed(self, row: int, col: int, plant_name: str):
        """
        Notify all observers that a plant has been placed.

        Preconditions:
            - The plant must be placed at valid coordinates
            - The plant name must be valid

        Parameters:
            row (int): The row coordinate of the plant
            col (int): The column coordinate of the plant
            plant_name (str): The name of the plant being placed
        """
        pass

    @abstractmethod
    def notify_plant_removed(self, row: int, col: int, plant_name: str):
        """
        Notify all observers that a plant has been removed.
        
        Preconditions:
            - The plant must be removed from valid coordinates
            - The plant name must be valid

        Parameters:
            row (int): The row coordinate of the plant
            col (int): The column coordinate of the plant
            plant_name (str): The name of the plant being removed
        """
        pass
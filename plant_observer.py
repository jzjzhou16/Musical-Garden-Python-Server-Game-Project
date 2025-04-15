from abc import abstractmethod
from typing import Protocol

# abstract observer class for the observer pattern
class PlantObserver(Protocol):
    """
    Abstract class representing an observer in the observer pattern.
    It defines the methods for receiving notifications about plant placement and removal.

    Parameters:
        row (int): The row coordinate of the plant
        col (int): The column coordinate of the plant
        plant_name (str): The name of the plant being placed or removed
    """
    @abstractmethod
    def on_plant_placed(self, row: int, col: int, plant_name: str) -> None:
        """
        Notify the observer that a plant has been placed.

        Preconditions:
            - The plant must be placed at valid coordinates
            - The plant name must be valid
        Postconditions:
            - The observer is notified of the plant placement
            - The state of the observer may change based on the plant placement
        
        Parameters:
            row (int): The row coordinate of the plant
            col (int): The column coordinate of the plant
            plant_name (str): The name of the plant being placed
        """
        pass
    
    @abstractmethod
    def on_plant_removed(self, row: int, col: int, plant_name: str) -> None:
        """
        Notify the observer that a plant has been removed.

        Preconditions:
            - The plant must be removed from valid coordinates
            - The plant name must be valid
        Postconditions:
            - The observer is notified of the plant removal
            - The state of the observer may change based on the plant removal

        Parameters:
            row (int): The row coordinate of the plant
            col (int): The column coordinate of the plant
            plant_name (str): The name of the plant being removed
        """
        pass
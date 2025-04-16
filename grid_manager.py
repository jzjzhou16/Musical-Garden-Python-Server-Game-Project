from .imports import *
from typing import TYPE_CHECKING,List, Optional
from .plant_observer import PlantObserver
from .garden_grid import GardenGrid
from .plants import Plant

if TYPE_CHECKING:
    from tiles.map_objects import *

# implements the observer pattern
# when a plant is placed or removed, the grid manager is notified
class GridManager(PlantObserver):
    """
    Manages the grid of notes in the garden grid
    Dynamically creates a grid of notes based on the garden grid size and the plants placed on it.
    Implements the observer pattern to update the grid when plants are placed or removed.

    Parameters:
        garden_grid (GardenGrid): The garden grid object to manage
        notes_grid (List[List[Optional[str]]]): A 2D list representing the grid of notes
        grid_origin (Coord): The origin coordinates of the grid
        _instance (GridManager): Singleton instance of the GridManager

    Attributes:
        PLANT_NOTES (Dict[str, str]): A dictionary mapping plant names to musical notes
        ROW_OCTAVES (List[int]): A list of octaves for each row in the grid
    """
    PLANT_NOTES = {
        "rose": "A",
        "tulip": "B",
        "daisy": "C",
        "sunflower": "D",
        "iris": "E",
        "lilac": "F",
        "orchid": "G",
    }
    ROW_OCTAVES = [2, 3, 4, 5]

    _instance = None
    
    @classmethod
    def get_instance(cls):
        """
        Returns the singleton instance of the GridManager.
        If the instance does not exist, it creates a new one.

        Preconditions:
            - The class must be initialized
        Postconditions:
            - The class is initialized and the instance is created
            - The instance is returned

        Parameters:
            cls (type): The class itself

        Returns:
            (GridManager): The singleton instance of the GridManager
        """
        #precondition
        assert cls._instance is not None, "GridManager must be initialized before use"
        return cls._instance

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the GridManager if it does not exist.
        If it exists, it returns the existing instance.

        Parameters:
            cls (type): The class itself
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            (GridManager): The singleton instance of the GridManager
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, garden_grid : GardenGrid) -> None:
        """
        Initializes the GridManager with a garden grid.
        Only once due to the singleton pattern.

        Preconditions:
            - The garden grid must be an instance of GardenGrid
        Postconditions:
            - The notes grid is initialized as a 2D list of None values
            - The grid origin is set to the garden grid's origin
            - The garden grid is attached to the GridManager

        Parameters:
            garden_grid (GardenGrid): The garden grid object to manage
        """
        #precondition
        assert isinstance(garden_grid, GardenGrid), "garden_grid must be an instance of GardenGrid"
        if not hasattr(self, '_initialized'):
            self.garden_grid = garden_grid
            # dynamically create a grid of notes based on any grid size
            self.notes_grid: List[List[Optional[str]]] = [
                [None]*garden_grid.grid_cols 
                for i in range(garden_grid.grid_rows)
            ]
            self.grid_origin = garden_grid.get_grid_origin()
            
            garden_grid.attach(self)
            self._initialized = True
            #postconditions
            assert self.notes_grid is not None, "notes_grid must be initialized"
            assert self.grid_origin is not None, "grid_origin must be initialized"

    def _convert_to_grid_coords(self, row: int, col: int) -> tuple[int, int]:
        """
        Converts absolute coordinates to grid coordinates.

        Preconditions:
            - The row and column coordinates must be valid
        Postconditions:
            - The grid coordinates are calculated based on the grid origin
            - The grid coordinates are returned as a tuple

        Parameters:
            row (int): The absolute row coordinate
            col (int): The absolute column coordinate

        Returns:
            (tuple[int, int]): The grid coordinates
        """
        return row - self.grid_origin.y, col - self.grid_origin.x
    
    def on_plant_placed(self, row: int, col: int, plant_name: str):
        """
        Called when a plant is placed in the garden grid.
        Updates the notes grid with the plant name.
        Dynamically searches for the note in the grid based on coordinates.

        Parameters:
            row (int): The row coordinate of the plant
            col (int): The column coordinate of the plant
            plant_name (str): The name of the plant being placed

        Preconditions:
            - The plant name must be valid
        Postconditions:
            - The notes grid is updated with the plant name
            - The state of the notes grid may change based on the plant placement
        """
        # dynamically search for note in the grid based on coords
        grid_row, grid_col = self._convert_to_grid_coords(row, col)
        self.notes_grid[grid_row][grid_col] = plant_name.lower()
        #postconditions
        assert self.notes_grid[grid_row][grid_col] == plant_name.lower(), "Notes grid not updated correctly"
            
    
    def on_plant_removed(self, row: int, col: int, plant_name: str) -> None:
        """
        Called when a plant is removed from the garden grid.
        Updates the notes grid to remove the plant name.
        Dynamically searches for the note in the grid based on coordinates.

        Parameters:
            row (int): The row coordinate of the plant
            col (int): The column coordinate of the plant
            plant_name (str): The name of the plant being removed

        Preconditions:
            - The plant name must be valid
        Postconditions:
            - The notes grid is updated to remove the plant name
            - The state of the notes grid may change based on the plant removal
        """
        # dynamically search for note in the grid based on coords
        #preconditions
        assert plant_name.lower() in self.PLANT_NOTES, "Invalid plant name"
        grid_row, grid_col = self._convert_to_grid_coords(row, col)
        self.notes_grid[grid_row][grid_col] = None
        #postconditions
        assert self.notes_grid[grid_row][grid_col] is None, "Notes grid updated correctly"
            

    def clear_all_plants(self, map: Map) -> list[Message]:
        """
        Clears all plants from the garden grid and the notes grid.
        Removes all plant objects from the map and clears the notes grid.
        
        Parameters:
            map (Map): The map object to remove plants from
        
        Preconditions:
            - The map must be an instance of Map
        Postconditions:
            - All plant objects are removed from the map
            - The notes grid is cleared
            - The state of the map and notes grid is updated

        Returns:
            (list[Message]): List of messages generated by removing plants
        """
        #preconditions
        assert isinstance(map, Map), "map must be an instance of Map"
        messages = []
        origin_x, origin_y = self.grid_origin.x, self.grid_origin.y
        
        for grid_row in range(len(self.notes_grid)):
            for grid_col in range(len(self.notes_grid[0])):
                if self.notes_grid[grid_row][grid_col] is not None:
                    # Convert grid coords back to absolute coords
                    abs_y = origin_y + grid_row
                    abs_x = origin_x + grid_col
                    coord = Coord(abs_y, abs_x)
                    
                    # Remove all plant objects at this coordinate
                    objects = map.get_map_objects_at(coord)
                    for obj in objects:
                        if isinstance(obj, ExtDecor | Plant):
                            map.remove_from_grid(obj, coord)
                    
                    # Clear the note
                    self.notes_grid[grid_row][grid_col] = None
        
        messages += map.send_grid_to_players()
        #postconditions
        assert self.notes_grid == [[None]*self.garden_grid.grid_cols for _ in range(self.garden_grid.grid_rows)], "Notes grid cleared correctly"
        return messages
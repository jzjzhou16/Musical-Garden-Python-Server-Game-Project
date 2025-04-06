from .imports import *
from typing import TYPE_CHECKING,List, Optional
from .GardenGrid import GardenGrid
from .Observer import PlantObserver

if TYPE_CHECKING:
    from tiles.map_objects import *

# implements the observer pattern
# when a plant is placed or removed, the grid manager is notified
class GridManager(PlantObserver):
    # this information is used within pressure plate to play sounds based on their location and flower
    # each note within the grid is represented by a letter
    PLANT_NOTES = {
        "rose": "A",
        "tulip": "B",
        "daisy": "C",
        "sunflower": "D",
        "iris": "E",
        "lilac": "F",
        "orchid": "G",
    }
    # each row is represented by an octave
    ROW_OCTAVES = [2, 3, 4, 5]

    _instance = None
    
    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.notes_grid = [[None]*12 for _ in range(4)]
        return cls._instance

    def __init__(self, garden_grid):
        if not hasattr(self, '_initialized'):
            if not isinstance(garden_grid, GardenGrid):
                raise ValueError("GridManager requires a GardenGrid instance")
            garden_grid.attach(self)
            print(f"GridManager initialized with garden grid at {id(garden_grid)}")
            self._initialized = True


    def update_grid(self, new_grid: List[List[Optional[str]]]):
        self.notes_grid = new_grid
        self.grid = new_grid
    
    # when plant is placed used for observer
    def on_plant_placed(self, row: int, col: int, plant_name: str):
        self.notes_grid[row - 1 ][col - 1] = plant_name
    
    # when plant is removed, used for observer
    def on_plant_removed(self, row: int, col: int, plant_name: str) -> None:
        self.notes_grid[row - 1][col - 1] = None

    def clear_all_plants(self, map: Map) -> list[Message]:
        messages = []
        for row in range(len(self.notes_grid)):
            for col in range(len(self.notes_grid[0])):
                if self.notes_grid[row][col] is not None:
                    # Convert grid coords to absolute room coords
                    abs_y = 1 + row  # Adjust based on your grid's origin
                    abs_x = 1 + col
                    coord = Coord(abs_y, abs_x)
                    
                    # Remove all plant objects at this coordinate
                    objects = map.get_map_objects_at(coord)
                    for obj in objects:
                        if isinstance(obj, ExtDecor):  # Check for plant types
                            map.remove_from_grid(obj, coord)
                    
                    # Clear the note
                    self.notes_grid[row][col] = None
        
        messages += map.send_grid_to_players()
        return messages
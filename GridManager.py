from .imports import *
from typing import TYPE_CHECKING,List, Optional
from .plantobserver import PlantObserver
from .gardengrid import GardenGrid

if TYPE_CHECKING:
    from tiles.map_objects import *

# implements the observer pattern
# when a plant is placed or removed, the grid manager is notified
class GridManager(PlantObserver):
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
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, garden_grid : GardenGrid):
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

    def _convert_to_grid_coords(self, row: int, col: int) -> tuple[int, int]:
        return row - self.grid_origin.y, col - self.grid_origin.x
    
    def on_plant_placed(self, row: int, col: int, plant_name: str):
        # dynamically search for note in the grid based on coords
        grid_row, grid_col = self._convert_to_grid_coords(row, col)
        self.notes_grid[grid_row][grid_col] = plant_name
            
    
    def on_plant_removed(self, row: int, col: int, plant_name: str) -> None:
        # dynamically search for note in the grid based on coords
        grid_row, grid_col = self._convert_to_grid_coords(row, col)
        self.notes_grid[grid_row][grid_col] = None
            

    def clear_all_plants(self, map: Map) -> list[Message]:
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
                        if isinstance(obj, ExtDecor):
                            map.remove_from_grid(obj, coord)
                    
                    # Clear the note
                    self.notes_grid[grid_row][grid_col] = None
        
        messages += map.send_grid_to_players()
        return messages
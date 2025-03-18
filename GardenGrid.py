from .imports import *
from typing import TYPE_CHECKING, List, Optional
from .my_greenhouse_MapObjects import Plant
from .my_greenhouse_MapObjects import PlantFactory
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

# helper class to represent a single cell in the garden grid strucutre
class GardenGridCell(MapObject):
    def __init__(self, parent: "GardenGrid", row: int, col: int) -> None:
        # Use the parent's image name (e.g. "tile/background/cobblestone")
        super().__init__(parent.get_image_name(), passable=True, z_index=parent.get_z_index())
        self.parent = parent
        self.row = row
        self.col = col

    def _get_tilemap(self) -> tuple[List[List[MapObject]], int, int]:
        # A single cell is just 1x1 and doesn’t need its own grid.
        return [[self]], 1, 1

class GardenGrid(MapObject):
    def __init__(self, image_name: str, grid_rows: int = 5, grid_cols: int = 8) -> None:
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.players_in_grid = set()
        super().__init__(f'tile/background/{image_name}', passable = True, z_index = 0)
        
        
        # grid_state is a 2D list, each cell may only hold one plant
        self.grid_state: List[List[Optional[Plant]]] = [[None for _ in range(grid_cols)] for _ in range (grid_rows)]


    def _get_tilemap(self) -> tuple[List[List[MapObject]], int, int]:
        tilemap: List[List[MapObject]] = []
        for i in range(self.grid_rows):
            row: List[MapObject] = []
            for j in range(self.grid_cols):
                cell = GardenGridCell(self, i, j)
                row.append(cell)
            tilemap.append(row)
        return tilemap, self.grid_rows, self.grid_cols

    def player_entered(self, player: HumanPlayer) -> list[Message]:
        # if player is already in the grid, return no message
        if player in self.players_in_grid:
            return []
        # else, add the player and send the welcome message
        self.players_in_grid.add(player)
        return [DialogueMessage(self,player, "Welcome, You are in the Garden Grid.", "cobblestone")]
    
    def player_exited(self, player: HumanPlayer) -> list[Message]:
            # when a player leaves the grid, remove them from the method, so re-entry will trigger the message again
            if player in self.players_in_grid:
                self.players_in_grid.remove(player)
                return [DialogueMessage(self,player, "You have left the garden grid", "cobblestone")]
            return []
    
    
    def place_plant(self, row: int, col: int, plant: Plant) -> bool:
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            # can plant if the cell is empty
            if self.grid_state[row][col] is None:
                self.grid_state[row][col] = plant
                return True
        return False
         
    def remove_plant(self, row: int, col: int) -> bool:
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            if self.grid_state[row][col] is not None:
                self.grid_state[row][col] = None
                return True
        return False
    
    def get_plant(self, row:int, col: int):
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            return self.grid_state[row][col]
        return None
    
    

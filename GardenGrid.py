from .imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class GardenGrid(MapObject):
    def __init__(self, grid_rows: int = 7, grid_cols: int = 12, cell_size: int = 32) -> None:
        super().__init__("coin", passable = True, z_index = 0)
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = cell_size
        # grid_state is a 2D list, each cell may only hold one plant

    def player_entered(self, player) -> list:
        return [DialogueMessage(self,player, "Welcome, You are in the Garden Grid.", "coin")]
    

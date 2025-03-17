from .imports import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class GardenGrid(MapObject):
    
    def __init__(self, image_name, grid_rows: int = 7, grid_cols: int = 12, cell_size: int = 32) -> None:
        super().__init__(f'tile/background/{image_name}', passable = True, z_index = 0)
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = cell_size

        self.players_in_grid = set()
        # grid_state is a 2D list, each cell may only hold one plant

    def player_entered(self, player) -> list:
        # if player is already in the grid, return no message
        if player in self.players_in_grid:
            return []
        # else, add the player and send the welcome message
        self.players_in_grid.add(player)
        return [DialogueMessage(self,player, "Welcome, You are in the Garden Grid.", "coin")]
    
    def player_exited(self, player) -> list:
            # when a player leaves the grid, remove them from the method, so re-entry will trigger the message again
            if player in self.players_in_grid:
                self.players_in_grid.remove(player)
                return [DialogueMessage(self,player, "You have left the garden grid", "coin")]
    
            return []

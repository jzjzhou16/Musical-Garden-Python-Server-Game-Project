from .imports import *
from typing import TYPE_CHECKING, List, Optional, Dict
from .GridCellFactory import GridCellFactory
from .my_greenhouse_MapObjects import Plant
from .my_greenhouse_MapObjects import PlantFactory

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class GardenGrid(MapObject):
    def __init__(self, image_name: str, position: Coord, grid_rows: int, grid_cols: int) -> None:
        # ensure that these instance variables are initialized before the mapObject is initialized.
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.players_in_grid = set()
        self.image_name = image_name
        # Store the grid origin, where it starts
        self.grid_origin = position
        # Initialize the GridCellFactory with the image name
        self.cell_factory = GridCellFactory(image_name)
        # Set garden grid position
        self.set_position(position)
        # grid_state is a 2D list, each cell may only hold one plant
        self.grid_state: List[List[Optional[Plant]]] = [[None for _ in range(grid_cols)] for _ in range (grid_rows)]
        
        super().__init__(f'tile/background/{image_name}', passable = True, z_index = 0)


    def _get_tilemap(self) -> tuple[List[List[MapObject]], int, int]:
        # tilemap, where each cell is being treated as a separate tile for rendering and other actions
        tilemap: List[List[MapObject]] = []
        for i in range(self.grid_rows):
            row: List[MapObject] = []
            for j in range(self.grid_cols):
                # Create a new tile for each grid cell from flyweight
                cell = self.cell_factory.get_cell(self.image_name)
                if cell:
                    row.append(cell)
            tilemap.append(row)
        return tilemap, self.grid_rows, self.grid_cols
    
    def get_grid_origin(self) -> Coord:
        return self.grid_origin
    
   




    def player_entered(self, player: HumanPlayer) -> list[Message]:
        # if player is already in the grid, return no message
        if player in self.players_in_grid:
            return []
        # else, add the player and send the welcome message
        self.players_in_grid.add(player)
        return [DialogueMessage(self,player, "Welcome, You are in the Garden Grid.", "")]
    
    def player_exited(self, player: HumanPlayer) -> list[Message]:
            # when a player leaves the grid, remove them from the method, so re-entry will trigger the message again
            if player in self.players_in_grid:
                self.players_in_grid.remove(player)
                return [DialogueMessage(self,player, "You have left the garden grid", "")]
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
    
    

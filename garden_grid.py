from .imports import *
from typing import TYPE_CHECKING, List, Optional, Dict
from .grid_cell import GridCellFactory
from .plants import Plant
from .plant_observer import PlantObserver
from .background_type import EmoteType
from .plant_subject import PlantSubject

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class GardenGrid(MapObject, PlantSubject):
    def __init__(self, image_name: str, position: Coord, grid_rows: int, grid_cols: int) -> None:
        self._observers: List[PlantObserver] = [] 
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

    def attach(self, observer: PlantObserver):
        if not hasattr(observer, 'on_plant_placed') or not hasattr(observer, 'on_plant_removed'):
            raise TypeError("Observer must implement PlantObserver protocol")
        self._observers.append(observer)
    
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
        messages = []
        # if player is already in the grid, return no message
        if player in self.players_in_grid:
            return []
        # else, add the player and send the welcome message
        self.players_in_grid.add(player)
        origin = self.get_grid_origin()
        coordinates = [(origin.y, origin.x-1), (origin.y+1, origin.x-1), (origin.y+2, origin.x-1), (origin.y+3, origin.x-1),(origin.y+4, origin.x-1),
                       (origin.y+5, origin.x-1), (origin.y+5, origin.x), (origin.y+5, origin.x+1), (origin.y+5, origin.x+2),(origin.y+5, origin.x+3),
                       (origin.y+5, origin.x+4),(origin.y+5, origin.x+5), (origin.y+5, origin.x+6), (origin.y+5, origin.x+7), (origin.y+5, origin.x+8),
                       (origin.y+5, origin.x+9), (origin.y+5, origin.x+10), (origin.y+5, origin.x+11),(origin.y+5, origin.x+12),(origin.y+4, origin.x+12),
                       (origin.y+3, origin.x+12), (origin.y+2, origin.x+12), (origin.y+1, origin.x+12), (origin.y, origin.x+12)]
        
        for y, x in coordinates:
            emote = EmoteType.get_random_emote_type()
            messages.append(EmoteMessage(self, player, emote, Coord(y,x)))
        return messages
    
    def player_exited(self, player: HumanPlayer) -> list[Message]:
            # when a player leaves the grid, remove them from the method, so re-entry will trigger the message again
            if player in self.players_in_grid:
                self.players_in_grid.remove(player)
                
            return []
    
    def get_plant(self, row:int, col: int):
        if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            return self.grid_state[row][col]
        return None

    def notify_plant_placed(self, row: int, col: int, plant_name: str):
        for observer in self._observers:
            if hasattr(observer, 'on_plant_placed'):
                observer.on_plant_placed(row, col, plant_name)

    def notify_plant_removed(self, row: int, col: int, plant_name: str):
        for observer in self._observers:
            if hasattr(observer, 'on_plant_removed'):
                observer.on_plant_removed(row, col, plant_name)


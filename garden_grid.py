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
    """
    A grid-based garden plot that manages plant placement and player interactions 
    
    Combines MapObject functionality with a PlantSubject observer pattern to:
        - Track plant positions in a 2D grid
        - Handle player entry/exit events
        - Notify observers of plant changes 

    Invariants:
        - grid_rows and grid_cols > 0 
        - grid_origin must be a valid Coord object
        - players_in_grid can only contain HumanPlayer instances
        - _observers can only contain PlantObserver instances
 
    """

    def __init__(self, image_name: str, position: Coord, grid_rows: int, grid_cols: int) -> None:
        """
        Initializes the garden grid with specified dimensions and position

        Preconditions:
            - image_name is a non-empty string
            - position is a valid Coord object
            - grid_rows > 0
            - grid_cols > 0

        Parameters:
            image_name (str): Base image for grid cells
            position (Coord): Initial coordinates of grid (top-left corner)
            grid_rows (int): Number of rows in the grid
            grid_cols (int): Number of columns in the grid
        """

        #preconditions
        assert isinstance(image_name, str) and len(image_name) > 0, "image_name must be a non-empty string"
        assert hasattr(position, 'x') and hasattr(position, 'y'), "position must be a valid Coord object"
        assert grid_rows > 0, "grid_rows must be a positive int"
        assert grid_cols > 0, "grid_cols must be a positive int"

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

        super().__init__(f'tile/background/{image_name}', passable = True, z_index = 0)

    def attach(self, observer: PlantObserver):
        """
        Registers an observer to receive plant change notifications.

        Preconditions: 
            - observer implements PlantObserver protocol

        Parameters:
            observer (PlantObserver): Object implementing PlantObserver protocol
            
        Raises:
            TypeError: If observer doesn't implement required methods
        """

        #preconditions
        if not hasattr(observer, 'on_plant_placed') or not hasattr(observer, 'on_plant_removed'):
                raise TypeError("Observer must implement PlantObserver protocol")
        
        self._observers.append(observer)

    def _get_tilemap(self) -> tuple[List[List[MapObject]], int, int]:
        """
        Generates a tilemap representation of the garden grid
        
        Returns:
            tuple: Containing...
                - 2D list of MapObjects representing each cell
                - Total # grid rows
                - Total # grid columns
        """

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
        """
        Returns the coordinates of the grid's top-left corner
        
        Returns:
            Coord: The origin position of the grid
        """
        return self.grid_origin 
    
    def player_entered(self, player: HumanPlayer) -> list[Message]:
        """
        Handles player entering the garden grid area

         Preconditions: 
            - player is a HumanPlayer instance

        Parameters:
            player (HumanPlayer): The player entering the grid
            
        Returns:
            list[Message]: Emote messages displayed around grid perimeter

        """

        #preconditions 
        assert isinstance(player, HumanPlayer), "player must be a HumanPlayer" 

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
        """
        Handles player exiting the garden grid area

        Preconditions: 
            - player is a HumanPlayer instance

        Parameters:
            player (HumanPlayer): The player entering the grid
         
        """

        #preconditions 
        assert isinstance(player, HumanPlayer), "player must be a HumanPlayer"

        # when a player leaves the grid, remove them from the method, so re-entry will trigger the message again
        if player in self.players_in_grid:
            self.players_in_grid.remove(player)
                
        return []
    

    def notify_plant_placed(self, row: int, col: int, plant_name: str):
        """
        Notifies observers when a plant is placed in the grid

         Preconditions:
            - 0 <= row < self.grid_rows
            - 0 <= col < self.grid_cols
            - plant_name must be a non-empty string
            - All observers must implement from PlantObserver
        
        Parameters:
            row (int): Grid row where plant was placed
            col (int): Grid column where plant was placed
            plant_name (str): Name of the planted item's image
        """

        #preconditions
        assert 0 <= row < self.grid_rows, "row is out of bounds"
        assert 0 <= col < self.grid_cols, "col is out of bounds"
        assert isinstance(plant_name, str) and len(plant_name) > 0, "plant_name must be a non-empty string"
        assert all(hasattr(o, 'on_plant_placed') for o in self._observers), "All observers must implement from PlantObserver"

        for observer in self._observers:
            if hasattr(observer, 'on_plant_placed'):
                observer.on_plant_placed(row, col, plant_name)

    def notify_plant_removed(self, row: int, col: int, plant_name: str):
        """

        Preconditions:
            - 0 <= row < self.grid_rows
            - 0 <= col < self.grid_cols
            - plant_name must be a non-empty string
            - All observers must implement from PlantObserver
        
        Parameters:
            row (int): Grid row where plant was removed
            col (int): Grid column where plant was removed
            plant_name (str): Name of the removed item's image 
        """

        #preconditions
        assert 0 <= row < self.grid_rows, "row out of bounds"
        assert 0 <= col < self.grid_cols, "col out of bounds"
        assert isinstance(plant_name, str) and len(plant_name) > 0, "plant_name must be non-empty string"
        assert all(hasattr(o, 'on_plant_removed') for o in self._observers), "All observers must implement PlantObserver"
 
        for observer in self._observers:
            if hasattr(observer, 'on_plant_removed'):
                observer.on_plant_removed(row, col, plant_name)

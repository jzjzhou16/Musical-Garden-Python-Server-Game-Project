from .imports import *
from typing import TYPE_CHECKING
from .garden_grid import *
from .plants import PlantFactory
from .background_type import Background, BackgroundFactory
from .pressure_plate import ColumnPressurePlate, ClearPressurePlate
from .grid_manager import GridManager
from .buttons import Shovel


if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class ExampleHouse(Map):
    """
    A map displaying an interactive musical garden 
    
    This map contains:
    - A garden grid for musical plant placement
    - Various interactive objects for instructions (board, NPC and signs)
    - Shovel and Clear buttons  
    - Doors to DemoRoom and TrottierTown 
    - Plant shelf for note selection
    
    Parameters:
        MAIN_ENTRANCE (bool): Class constant 
        garden_grid (GardenGrid): The main interactive garden grid area (where user can plant plants)
        grid_manager (GridManager): Manages grid interactions and sets/updates state
        npc (NPC): The instructional NPC character
    """

    MAIN_ENTRANCE = True

    def __init__(self) -> None:
        """Initializes the ExampleHouse with a garden grid, NPC, and base map properties."""

        #create garden grid 
        self.garden_grid = GardenGrid("dirt3", Coord(2,1), 4, 12)

        # create grid manager
        self.grid_manager = GridManager(self.garden_grid)
        
        # constructs NPC
        self.npc = NPC(
                name="Professor",
                image="prof",
                encounter_text="Welcome to the musical garden! Plant flowers from the shelf by pickung up (SPACE), and click again to plant it on garden grid!",
            )
    

        super().__init__(
            name="Test House",
            description="Welcome to the Musical Garden",
            size=(17, 15),
            entry_point=Coord(14, 7),
            background_tile_image = "grass",
        )

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        """Generates and places all objects in the ExampleHouse map
        
        Returns:
            list[tuple[MapObject, Coord]]: A list of tuples containing map objects and their map coordinates 
        """

        objects: list[tuple[MapObject, Coord]] = []
        
        for y in range(17):
            for x in range(15):
                if (y, x) == (16, 7):  
                    continue
            
                #set randomized background w/ flyweight factory
                background_tile = BackgroundFactory.get_background()
                objects.append((background_tile, Coord(y, x)))

        self.create_paths(objects)
        
        # add doors 
        door = Door('int_entrance', linked_room="Trottier Town", is_main_entrance=True)
        objects.append((door, Coord(16, 7)))
 
        demoRoomDoor = Door('empty', linked_room = "Demo Room")
        objects.append((demoRoomDoor, Coord(16,1)))

        #add tree
        tree = ExtDecor(image_name='Oak_Tree')
        objects.append((tree, Coord(6,0)))

        #instructions bulletin board 
        instructionsBoard = Sign('board_bulletin', "Note: Each row of the garden grid represents a different octave, while each plant corresponds to a note (A-G).")
        objects.append((instructionsBoard, Coord(7,4)))

        #instructions sign
        instructionsSign = Sign('sign', "Step onto the X button to clear all plants off your garden grid, and pick up (press SPACE at) the shovel to delete individual plants.")
        objects.append((instructionsSign, Coord(8,10)))

        
        #add greenhouse image (demo room)
        demoRoom = ExtDecor("House") 
        objects.append((demoRoom, Coord(9,0)))

        #add shovel
        shovel = Shovel("Shovel")
        objects.append((shovel, Coord(8,13)))

        #add play button row
        for col in range(12):
            plate = ColumnPressurePlate(col)
            objects.append((plate, Coord(x=col + 1, y=1)))

        #add clear button
        clear_plate = ClearPressurePlate()
        objects.append((clear_plate, Coord(7, 13)))
 
        #create plant shelf:
        plant_coords = [
            Coord(9, 13),  # Rose
            Coord(10, 13),  # Tulip
            Coord(11, 13),  # Daisy
            Coord(12, 13), # Sunflower
            Coord(13, 13), # Iris
            Coord(14, 13), # lilac
            Coord(15, 13)  # Orchid
        ]

        for coord in plant_coords:
            background_tile = Background("wood_planks")  
            objects.append((background_tile, coord))

        for plant_name, coord in [("rose", Coord(9, 13)), ("tulip", Coord(10, 13)), 
                                  ("daisy", Coord(11, 13)), ("sunflower", Coord(12, 13)), 
                                  ("iris", Coord(13, 13)), ("lilac", Coord (14, 13)), ("orchid", Coord(15, 13))]:
            plant = PlantFactory.get_plant(plant_name)
            if plant:
                objects.append((plant, coord))

        # add npc
        objects.append((self.npc, Coord(13, 10)))

        # add grid cells        
        tilemap, rows, cols = self.garden_grid._get_tilemap()
        grid_origin = self.garden_grid.get_grid_origin()  
        
        for i in range(rows):
            for j in range(cols):
                cell = tilemap[i][j]
                cell_coord = Coord(grid_origin.y + i, grid_origin.x + j)  
                objects.append((cell, cell_coord))

        return objects

    def create_paths(self, objects: list) -> None:
        """Creates visual navigable paths throughout the house map by altering the pre-defined (and randomized) background types  
        
        Parameters:
            objects (list[tuple[MapObject, Coord]]): The list of objects to append path tiles to (so that they show up on the map visually)
        """

        path_cell = BackgroundFactory.get_background("path")
        path_left = BackgroundFactory.get_background("left")
        path_right = BackgroundFactory.get_background("right")
        path_top = BackgroundFactory.get_background("top")
        path_bottom = BackgroundFactory.get_background("bottom")

        for y in range(6, 15):
            objects.append((path_left, Coord(y, 6)))     
            objects.append((path_cell, Coord(y, 7)))     
            objects.append((path_cell, Coord(y, 8)))     
            objects.append((path_right, Coord(y, 9)))    
        
        for x in range(7, 9):
            objects.append((path_top, Coord(4, x)))       

        path_to_house = [
            (path_left, 15, 1), (path_right, 15, 2),
            (path_left, 15, 6), (path_cell, 15, 7), (path_cell, 15, 8), (path_right, 15, 9),
            (path_left, 16, 1), (path_cell, 16, 2),
            (path_top, 16, 3), (path_top, 16, 4), (path_top, 16, 5),
            (path_cell, 16, 6), (path_cell, 16, 7), (path_cell, 16, 8), (path_right, 16, 9)
        ]

        for tile, y, x in path_to_house:
            objects.append((tile, Coord(y, x)))

        #path to plant shelf
        for y in range(10, 13):
            objects.append((path_cell, Coord(y, 9)))

        for x in range(10, 13):
            objects.append((path_top, Coord(10, x)))    
            objects.append((path_cell, Coord(11, x)))   
            objects.append((path_bottom, Coord(12, x)))  

    def move(self, player: HumanPlayer, direction_s: str) -> list[Message]:
        """
        Handles player movement and updates garden state accordingly
        
        Parameters:
            player (HumanPlayer): The player/user who is moving
            direction_s (str): The user's direction of movement ('up', 'down', 'left', 'right')
            
        Returns:
            list[Message]: Message generated by the movement and garden state updates
        """
        messages = super().move(player, direction_s)
        garden_messages = self.update_player_in_garden(player)
        messages.extend(garden_messages)
        return messages
 
    def update_player_in_garden(self,player:HumanPlayer) -> list[Message]:
        """
        Updates garden state based on the player's position
        
        Parameters:
            player (HumanPlayer): The player/user to check position for
            
        Returns:
            list[Message]: Message generated based on whether the user is entering/exiting the garden area
        """

        messages = []
        player_pos = player.get_current_position()
        grid_origin = self.garden_grid.get_grid_origin()
        grid_columns = self.garden_grid.grid_cols
        grid_rows = self.garden_grid.grid_rows
        
        # Check if player's coordinates are within the garden grid 
        in_garden = (grid_origin.x <= player_pos.x < grid_origin.x + grid_columns and
                     grid_origin.y <= player_pos.y < grid_origin.y + grid_rows)
        
        if in_garden:
            messages = self.garden_grid.player_entered(player)
        
        else:
            messages = self.garden_grid.player_exited(player)
        
        return messages
    
    
    

        
        
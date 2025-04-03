from .imports import *
from .GardenGrid import *
from .GridCellFactory import GridCellFactory
from .NPCSingleton import NPCSingleton
from typing import TYPE_CHECKING
from .Plant import Plant, PlantFactory
from .BackgroundType import Background, BackgroundFactory
import random
from .PressurePlate import MusicalPressurePlate
from .GridManager import GridManager

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *



class ExampleHouse(Map):
    def __init__(self) -> None:
        #create garden grid 

        self.garden_grid = GardenGrid("dirt3", Coord(1,1), 4, 12)

        # create grid manager
        GridManager(self.garden_grid)
        
        # constructs NPC Singleton to have one instance of the grid exists at a time
        self.npc = NPCSingleton(
                name="Professor",
                image="prof",
                encounter_text="Welcome to the musical garden!",
                grid=self.garden_grid
            )
        
        # create pressure plate
        self.pressure_plate = MusicalPressurePlate()
        
        #background image options
        self.background_options = [
            'basicGrass',
            'flowerGrass',   
            'plantGrass',
            'stoneGrass',
        ]

        super().__init__(
            name="Test House",
            description="Welcome to the Musical Garden",
            size=(15, 15),
            entry_point=Coord(14, 7),
            background_tile_image = "basicGrass",
        )

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []
        
        #set randomized background w/ flyweight factory
        
        flyweight_tiles = {
            bg_type: BackgroundFactory.get_background(bg_type)
            for bg_type in self.background_options
        }

        for y in range(15):
            for x in range(15):
                if (y, x) == (14, 7):  
                    continue

                background_type = random.choice(self.background_options)
                background_tile = flyweight_tiles[background_type]   
                objects.append((background_tile, Coord(y, x)))

        self.create_paths(objects)
        
        # add doors
        door = Door('int_entrance', linked_room = "Trottier Town")
        objects.append((door, Coord(14, 7)))
        
        demoRoomDoor = Door('empty', linked_room = "demo_room")
        objects.append((demoRoomDoor, Coord(14,2)))

        #tree/plant decor 
        tree = ExtDecor('Oak_Tree')
        objects.append((tree, Coord(4,0)))

        #add greenhouse image (demo room)
        demoRoom = ExtDecor("House") 
        objects.append((demoRoom, Coord(7,0)))

        #add shovel
        shovel = ExtDecor("shovel1")
        objects.append((shovel, Coord(6,13)))

        #add play button 
        play_button = MusicalPressurePlate()
        objects.append((play_button, Coord(6,4))) 

        #create plant shelf:
        plant_coords = [
            Coord(7, 13),  # Rose
            Coord(8, 13),  # Tulip
            Coord(9, 13),  # Daisy
            Coord(10, 13), # Sunflower
            Coord(11, 13), # Lilac
            Coord(12, 13), # Iris
            Coord(13, 13)  # Orchid
        ]

        for coord in plant_coords:
            background_tile = Background("wood_planks")  
            objects.append((background_tile, coord))

        for plant_name, coord in [("Rose", Coord(7, 13)), ("Tulip", Coord(8, 13)), 
                                  ("Daisy", Coord(9, 13)), ("Sunflower", Coord(10, 13)), 
                                  ("Lilac", Coord(11, 13)), ("Iris", Coord (12, 13)), ("Orchid", Coord(13, 13))]:
            plant = PlantFactory.get_plant(plant_name)
            if plant:
                objects.append((plant, coord))

        # add npc singleton
        objects.append((self.npc, Coord(12, 5)))

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
        path_cell = BackgroundFactory.get_background("path")
        path_left = BackgroundFactory.get_background("left")
        path_right = BackgroundFactory.get_background("right")
        path_top = BackgroundFactory.get_background("top")
        path_bottom = BackgroundFactory.get_background("bottom")

        for y in range(4, 13):
            objects.append((path_left, Coord(y, 6)))     
            objects.append((path_cell, Coord(y, 7)))     
            objects.append((path_cell, Coord(y, 8)))     
            objects.append((path_right, Coord(y, 9)))    
        
        for x in range(7, 9):
            objects.append((path_top, Coord(4, x)))      
            objects.append((path_bottom, Coord(13, x)))  

        path_to_house = [
            (path_left, 13, 1), (path_right, 13, 2),
            (path_left, 13, 6), (path_cell, 13, 7), (path_cell, 13, 8), (path_right, 13, 9),
            (path_left, 14, 1), (path_cell, 14, 2),
            (path_top, 14, 3), (path_top, 14, 4), (path_top, 14, 5),
            (path_cell, 14, 6), (path_cell, 14, 7), (path_cell, 14, 8), (path_right, 14, 9)
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
 

    def update_player_in_garden(self,player:HumanPlayer) -> list[Message]:
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
    

        
        
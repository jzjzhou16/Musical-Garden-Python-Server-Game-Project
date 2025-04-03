from .imports import *
from .GardenGrid import *
from .GridCellFactory import GridCellFactory
from .NPCSingleton import NPCSingleton
from typing import TYPE_CHECKING
from .Plant import Plant, PlantFactory
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
            'plantGrass'
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

        #randomize background tiles (flowers, plants, normal grass)
        for y in range(15):   
            for x in range(15):   
                if (y, x) in [(14, 7)]:
                    continue
                    
                bg_image = random.choice(self.background_options)
                bg_tile = Background(bg_image)
                objects.append((bg_tile, Coord(y, x)))
        
        # add a door
        door = Door('int_entrance', linked_room = "Trottier Town")
        objects.append((door, Coord(14, 7)))
        
        demoRoomDoor = Door('empty', linked_room = "demo_room")
        objects.append((demoRoomDoor, Coord(14,2)))

        #add greenhouse image (demo room)
        demoRoom = ExtDecor("House") 
        objects.append((demoRoom, Coord(7,0)))

        #add shovel
        shovel = ExtDecor("shovel1")
        objects.append((shovel, Coord(6,13)))

        #add play button 
        play_button = MusicalPressurePlate()
        objects.append((play_button, Coord(6,1))) 

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

        #add paths:
        path_types = {
            'main': 'path',
            'left side': "left", 
            'right side': "right", 
            'top left corner': "topLeft", 
            'top right corner': "topRight", 
            'bottom right corner': "bottomRight", 
            'bottom left corner': "bottomLeft", 
            'bottom': "bottom",
            'top': "top",
            'stones': "stoneGrass"
        }

        path_coords = []

        for y in range(4, 14):
            objects.append((Background(path_types['left side']), Coord(y, 6)))
            objects.append((Background(path_types['main']), Coord(y, 7)))
            objects.append((Background(path_types['main']), Coord(y, 8)))
            objects.append((Background(path_types['right side']), Coord(y, 9)))

        for x in range(6, 10):
            objects.append((Background(path_types['top']), Coord(4, x)))   
            objects.append((Background(path_types['bottom']), Coord(13, x)))  

        return objects


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

        
        
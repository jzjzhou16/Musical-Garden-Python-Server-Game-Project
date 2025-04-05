from .imports import *
from .GardenGrid import *
from .GridCellFactory import GridCellFactory
from .NPCSingleton import NPCSingleton
from typing import TYPE_CHECKING
from .Plant import Plant, PlantFactory 
from .GridManager import GridManager
from .PlantAudios import plantAudios
from .BackgroundType import Background, BackgroundFactory
import random

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class DemoRoom(Map):
    def __init__(self) -> None:
        #create garden grids
        self.demo_grids = [
            GardenGrid("dirt3", Coord(1, 1), 4, 12),
            GardenGrid("dirt3", Coord(6, 1), 4, 12),
            GardenGrid("dirt3", Coord(11, 1), 4, 12)
        ]

        super().__init__(
            name="Demo House",
            size=(18, 16),
            entry_point=Coord(16, 1),
            description="Welcome to the Musical Garden Demo Room",
            background_tile_image = "basicGrass", 
        )

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        #create three garden grids (3 different demos )
        for garden in self.demo_grids:
            tilemap, rows, cols = garden._get_tilemap()
            grid_origin = garden.get_grid_origin()
            for i in range(rows):
                for j in range(cols):
                    cell = tilemap[i][j]
                    cell_coord = Coord(grid_origin.y + i, grid_origin.x + j)
                    objects.append((cell, cell_coord))

        #add plants
        demo_layouts = [ 
        # Demo 1 layout - happy bday
        { 
            Coord(3, 1): "Daisy",  # C
            Coord(3, 2): "Daisy",  # C
            Coord(3, 3): "Sunflower", #D
            Coord(3, 4): "Daisy",  # C
            Coord(3, 5): "Lilac",   # F
            Coord(3, 6): "Iris",   # E   
            Coord(3, 7): "Daisy",  # C
            Coord(3, 8): "Daisy",  # C
            Coord(3, 9): "Sunflower",# D
            Coord(3, 10): "Daisy",  # C
            Coord(3, 11): "Orchid",   # G
            Coord(3, 12): "Lilac",   # F 
        }, 
        # Demo 2 layout - twinkle twinkle little star
        { 
            Coord(13, 1): "Rose",    # A 
            Coord(13, 3): "Orchid",  # G
            Coord(13, 4): "Orchid",  # G 

            Coord(13, 6): "Daisy",   # C
            Coord(13, 7): "Daisy",   # C
            Coord(13, 8): "Orchid",  # G
            Coord(13, 9): "Orchid",  # G
            Coord(13, 10): "Rose",   # A
            Coord(13, 11): "Rose",   # A
            Coord(13, 12): "Orchid", # G
        }, 
        # Demo 3 layout - jingle bells
        { 
            Coord(8, 1): "Iris",     # E
            Coord(8, 2): "Iris",     # E
            Coord(8, 3): "Iris",     # E
            Coord(8, 4): "Iris",     # E
            Coord(8, 6): "Iris",     # E
            Coord(8, 7): "Iris",     # E
            Coord(8, 8): "Iris",     # E 
            Coord(8, 9): "Orchid",   # G
            Coord(8, 10): "Daisy",     # C 
            Coord(8, 11): "Sunflower", # D
            Coord(8, 12): "Iris",    # E
        }
        ]

        for layout in demo_layouts:
            for coord, plant_name in layout.items():
                plant = PlantFactory.get_plant(plant_name)
                if plant:
                    objects.append((plant, coord))

        #create background
        for y in range(18):
            for x in range(16):
                if (y, x) == (14, 7):  
                    continue
            
                #set randomized background w/ flyweight factory
                background_tile = BackgroundFactory.get_background()
                objects.append((background_tile, Coord(y, x)))

        # add a exit door back to room
        door = Door('houseDoor', linked_room="Example House", is_main_entrance=True)
        objects.append((door, Coord(16, 1)))
    
        #demo 1
        demo1Sign = Sign('sign', "Demo Track: Happy Birthday")
        demo1PlayButton = ExtDecor('playButton')

        objects.append((demo1Sign, Coord(3,14)))

        #demo 2
        demo2Sign = Sign('sign', "Demo Track: Twinkle Twinkle Little Star")
        objects.append((demo2Sign, Coord(8,14)))

        #demo 3
        demo3Sign = Sign('sign', "Demo Track: jingle bells")
        objects.append((demo3Sign, Coord(13,14)))

        return objects
     

 
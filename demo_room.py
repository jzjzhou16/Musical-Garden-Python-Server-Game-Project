from .imports import *
from .GardenGrid import *
from typing import TYPE_CHECKING
from .buttons import *
from .BackgroundType import BackgroundFactory
from .PressurePlate import ColumnPressurePlate
from .GridManager import GridManager


if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class DemoRoom(Map):
    def __init__(self) -> None:
        #create garden grids
        self.demo_grids = [

            GardenGrid("dirt3", Coord(2, 1), 4, 12),
            GardenGrid("dirt3", Coord(8, 1), 4, 12),
            GardenGrid("dirt3", Coord(14, 1), 4, 12)
        ]
        
        super().__init__(
            name="Demo House",
            size=(21, 16),
            entry_point=Coord(19, 1),
            description="Welcome to the Musical Garden Demo Room",
            background_tile_image='grass',
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

        #create background
        for y in range(21):
            for x in range(16): 
            
                #set randomized background w/ flyweight factory
                background_tile = BackgroundFactory.get_background()
                objects.append((background_tile, Coord(y, x)))

        # add a exit door back to room
        door = Door('houseDoor', linked_room="Example House")
        objects.append((door, Coord(19, 1)))

        #instructions sign 
        demoInstructionsSign = Sign('sign', "Welcome to the Demo Room! Preview 3 classic tunes by pressing SPACE at each play button.")
        objects.append((demoInstructionsSign, Coord(19,4)))
    
        #demo 1
        demo1Sign = Sign('sign', "Demo Track: Happy Birthday")
        demo1PlayButton = PlayButton1('PlayButton')
        objects.append((demo1Sign, Coord(3,14)))
        objects.append((demo1PlayButton, Coord(4,14)))
        #demo 2
        demo2Sign = Sign('sign', "Demo Track: Twinkle Twinkle Little Star")
        demo2PlayButton = PlayButton2('PlayButton')
        objects.append((demo2Sign, Coord(9,14)))
        objects.append((demo2PlayButton, Coord(10,14)))
        #demo 3
        demo3Sign = Sign('sign', "Demo Track: jingle bells")
        demo3PlayButton = PlayButton3('PlayButton')
        objects.append((demo3Sign, Coord(15,14)))
        objects.append((demo3PlayButton, Coord(16,14)))

        return objects
     
    

 
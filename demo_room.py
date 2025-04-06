from .imports import *
from .GardenGrid import *
from typing import TYPE_CHECKING
from .Shovel import *
from .BackgroundType import BackgroundFactory
from .PressurePlate import ColumnPressurePlate

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class DemoRoom(Map):
    def __init__(self) -> None:
        #create garden grids
        self.demo_grids = GardenGrid("dirt3", Coord(1, 1), 4, 12)
        

        super().__init__(
            name="Demo House",
            size=(21, 16),
            entry_point=Coord(19, 1),
            description="Welcome to the Musical Garden Demo Room",
            background_tile_image = "basicGrass", 
        )
    def get_garden_grid(self) ->GardenGrid:
        return self.demo_grids

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        #create three garden grids (3 different demos )
        
        tilemap, rows, cols = self.demo_grids._get_tilemap()
        grid_origin = self.demo_grids.get_grid_origin()
        for i in range(rows):
            for j in range(cols):
                cell = tilemap[i][j]
                cell_coord = Coord(grid_origin.y + i, grid_origin.x + j)
                objects.append((cell, cell_coord))

        #create background
        for y in range(20):
            for x in range(16):
                # if (y, x) == (14, 7):  
                #     continue
            
                #set randomized background w/ flyweight factory
                background_tile = BackgroundFactory.get_background()
                objects.append((background_tile, Coord(y, x)))

        # add a exit door back to room
        door = Door('houseDoor', linked_room="Example House", is_main_entrance=True)
        objects.append((door, Coord(19, 1)))

        for col in range(12):
            plate = ColumnPressurePlate(col)
            objects.append((plate, Coord(x=col + 1, y=0)))
    
        #demo 1
        demo1Sign = Sign('sign', "Demo Track: Happy Birthday")
        demo1PlayButton = PlayButton1('PlayButton')
        objects.append((demo1Sign, Coord(9,14)))
        objects.append((demo1PlayButton, Coord(10,14)))
        #demo 2
        demo2Sign = Sign('sign', "Demo Track: Twinkle Twinkle Little Star")
        demo2PlayButton = PlayButton2('PlayButton')
        objects.append((demo2Sign, Coord(13,1)))
        objects.append((demo2PlayButton, Coord(13,2)))
        #demo 3
        demo3Sign = Sign('sign', "Demo Track: jingle bells")
        demo3PlayButton = PlayButton3('PlayButton')
        objects.append((demo3Sign, Coord(15,14)))
        objects.append((demo3PlayButton, Coord(15,15)))


        return objects
     

 
from .imports import *
from .GardenGrid import *
from .GridCellFactory import GridCellFactory
from .NPCSingleton import NPCSingleton
from typing import TYPE_CHECKING
from .Plant import Plant, PlantFactory 
import random

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class DemoRoom(Map):
    def __init__(self) -> None:
        #create garden grid 
        #self.garden_grid = GardenGrid("dirt3", Coord(1,1), 4, 12)
        
       #do we want to make another NPC?

        super().__init__(
            name="Demo House",
            size=(15, 15),
            entry_point=Coord(14, 2),
            description="Welcome to the Musical Garden Demo Room",
            background_tile_image = "wood_planks", 
        )

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        # add a exit door back to room
        door = Door('int_entrance', linked_room = "example_map")
        objects.append((door, Coord(14, 2)))

        return objects
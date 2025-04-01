from .imports import *
from typing import TYPE_CHECKING, List, Optional, Dict
from .GardenGrid import GardenGrid
from .Plant import Plant
from .Plant import PlantFactory

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class NPCSingleton(NPC):
    _instance = None
    name: str
    image: str
    encounter_text: str
    _grid: GardenGrid
    npc_coord: Coord

    def __new__(cls, *args, grid: Optional[GardenGrid] = None, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name: str, image: str, encounter_text: str, grid: GardenGrid, *args, **kwargs):
        if not hasattr(self, "_initialized"):
            super().__init__(name, image, encounter_text, *args, **kwargs)
    
            self._grid = grid
            self._initialized = True
            self.npc_coord = Coord(4, 1)
from .imports import *

from typing import TYPE_CHECKING
from typing import Dict

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *



class Plant(MapObject):
    def __init__(self, name: str, image: str, size: tuple[int, int]):
        self.name = name
        self.image = image  
        self.size = size

#Flyweight
class PlantFactory:
    _plants: Dict[str, Plant] = {}
    @staticmethod
    def getPlant(name: str) -> Plant | None:
        if name not in PlantFactory._plants:
            plant_info = {
                "Daisy": Plant("Daisy", "Daisy.png", (1, 1)),
                "Lilac": Plant("Lilac", "Lilac.png", (1, 1)),
                "Orchid": Plant("Orchid", "Orchid.png", (1, 1)),
                "Rose": Plant("Rose", "Rose.png", (1, 1)),
                "Sunflower": Plant("Sunflower", "Sunflower.png", (1, 1)),
                "Tulip": Plant("Tulip", "Tulip.png", (1, 1)),
            }
            if name in plant_info:
                PlantFactory._plants[name] = plant_info[name]
        return PlantFactory._plants.get(name)
                

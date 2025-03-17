from typing import TYPE_CHECKING
from typing import Dict
from .imports import *

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from maps.base import Map



class Plant(MapObject):
    def __init__(self, name: str, image: str) -> None:
        super().__init__(image, passable=True, z_index=1)
        self.__name = name
    
    def _get_image_size(self) -> tuple[int, int]:
        return (1,1)

    def get_name(self) -> str:
        return self.__name

#Flyweight
class PlantFactory:
    _plants: Dict[str, Plant] = {}
    @staticmethod
    def get_plant(name: str) -> Plant | None:
        if name not in PlantFactory._plants:
            plant_info = {
                "Daisy": Plant("Daisy", "Daisy.png"),
                "Lilac": Plant("Lilac", "Lilac.png"),
                "Orchid": Plant("Orchid", "Orchid.png"),
                "Rose": Plant("Rose", "Rose.png"),
                "Sunflower": Plant("Sunflower", "Sunflower.png"),
                "Tulip": Plant("Tulip", "Tulip.png"),
            }
            if name in plant_info:
                PlantFactory._plants[name] = plant_info[name]
        return PlantFactory._plants.get(name)
                

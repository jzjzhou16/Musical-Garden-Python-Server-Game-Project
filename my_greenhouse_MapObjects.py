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
    def __init__(self, image: str) -> None:
        super().__init__(f'tiles_output/{image}', passable=True, z_index=0)
        self.__image = image
    
    def _get_image_size(self) -> tuple[int, int]:
        return (1,1)

#Flyweight
class PlantFactory:
    _plants: Dict[str, Plant] = {}
    @staticmethod
    def get_plant(name: str) -> Plant | None:
        plant_info = {
                "Daisy": "Daisy.png",
                "Lilac": "Lilac.png",
                "Orchid": "Orchid.png",
                "Rose": "Rose.png",
                "Sunflower": "Sunflower.png",
                "Tulip":  "Tulip.png",
            }
        if name not in PlantFactory._plants:
            if name in plant_info:
                PlantFactory._plants[name] = Plant(plant_info[name])
        return PlantFactory._plants.get(plant_info[name])
                

from typing import TYPE_CHECKING
from typing import Dict, Optional
from .imports import *
from .PlayerCommand import pickUpPlantCommand

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from maps.base import Map

class Plant(MapObject):
    def __init__(self, image: str) -> None:
        super().__init__(image, passable=False, z_index=0)
        self.__image = image
    
    def _get_image_size(self) -> tuple[int, int]:
        return (1,1)
    
    def get_plant_name(self) -> str:
        return self.__image.replace(".png", "")
    
    def player_interacted(self, player: HumanPlayer, ) -> list[Message]:
        command = pickUpPlantCommand()
        plant_name = self.get_plant_name()
        return command.execute("pickup_plant", player.get_current_room(), player, plant_name)

#Flyweight
class PlantFactory:
    _plants: Dict[str, Plant] = {}
    @staticmethod
    def get_plant(name: str) -> Optional[Plant]:
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
            else:
                return None
        return PlantFactory._plants.get(name)
                

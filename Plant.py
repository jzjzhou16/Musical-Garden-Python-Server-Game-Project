from .imports import *
from typing import TYPE_CHECKING
from typing import Dict, Optional
from .pickUpCommand import pickUpPlantCommand

if TYPE_CHECKING:
    from tiles.base import MapObject
    from tiles.map_objects import *

class Plant(MapObject):
    def __init__(self, image: str) -> None:
        super().__init__(image, passable=False, z_index=0)
        self.__image = image
    
    # image is same size for all plants
    def _get_image_size(self) -> tuple[int, int]:
        return (1,1)
    
    def get_plant_name(self) -> str:
        return self.__image.replace(".png", "")
    
    # command pattern
    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        command = pickUpPlantCommand()
        plant_name = self.get_plant_name()
        player.set_state('carrying_plant', plant_name)
        return command.execute("pickup_plant", player.get_current_room(), player, plant_name)

#Flyweight
class PlantFactory:
    _plants: Dict[str, Plant] = {}
    # static because all plant factories refer to the same dictionary
    @staticmethod
    def get_plant(name: str) -> Optional[Plant]:
        plant_info = {
                "daisy": "Daisy.png",
                "lilac": "Lilac.png",
                "orchid": "Orchid.png",
                "rose": "Rose.png",
                "sunflower": "Sunflower.png",
                "tulip":  "Tulip.png",
                "iris": "Iris.png"
            }
        if name not in PlantFactory._plants:
            if name in plant_info:
                PlantFactory._plants[name] = Plant(plant_info[name])
            else:
                return None
        return PlantFactory._plants.get(name)
                

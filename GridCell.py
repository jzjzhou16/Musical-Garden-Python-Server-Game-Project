from .imports import *
from typing import TYPE_CHECKING, List, Optional, Dict
from .PlantInteractionCommand import PlantInteractionCommand

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *


class GridCell(MapObject):
    def __init__(self, image_name: str, passable: bool, z_index: int) -> None:
        # Call the MapObject constructor with a fixed image name, passable and z_index
        super().__init__(f'tile/background/{image_name}', passable, z_index)

    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        command = PlantInteractionCommand()
        return command.execute('plant_interaction', player.get_current_room(),player)
    
    def _get_tilemap(self) -> tuple[List[List[MapObject]], int, int]:
        # One cell
        return [[self]], 1, 1
    
from .imports import *
from typing import TYPE_CHECKING
from .pickUpCommand import pickUpShovelCommand

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from maps.base import Map

class Shovel(ExtDecor):
    def __init__(self, image: str) -> None:
        super().__init__(image)
        self.__image = image

    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        player.set_state('carrying_shovel', self.__image)
        command = pickUpShovelCommand()
        return command.execute("pickup_plant", player.get_current_room(), player, self.__image)
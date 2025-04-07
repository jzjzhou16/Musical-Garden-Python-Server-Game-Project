from .imports import *
from typing import TYPE_CHECKING
from .pickup_command import pickUpShovelCommand
from .demo_command import *

if TYPE_CHECKING:
    from tiles.map_objects import *

class Shovel(ExtDecor):
    def __init__(self, image: str) -> None:
        super().__init__(image)
        self.__image = image

    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        player.set_state('carrying_shovel', self.__image)
        command = pickUpShovelCommand()
        return command.execute("pickup_shovel", player.get_current_room(), player, self.__image)

class PlayButton1(ExtDecor):
    def __init__(self, image: str) -> None:
        super().__init__(image)
        self.__image = image

    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        command = happybirthdayCommand()
        return command.execute("happy_birthday", player.get_current_room(), player)

class PlayButton2(ExtDecor):
    def __init__(self, image: str) -> None:
        super().__init__(image)
        self.__image = image

    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        command = twinkleCommand()
        return command.execute("twinkle", player.get_current_room(), player)
    
class PlayButton3(ExtDecor):
    def __init__(self, image: str) -> None:
        super().__init__(image)
        self.__image = image

    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        command = jingleBellsCommand()
        return command.execute("jingle_bells", player.get_current_room(), player)
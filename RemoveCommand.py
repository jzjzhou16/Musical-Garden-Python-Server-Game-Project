from .imports import *
from typing import TYPE_CHECKING, Optional
from .Plant import PlantFactory, Plant

if TYPE_CHECKING:
    from command import ChatCommand
    from maps.base import Map
    from tiles.map_objects import *
    from .GardenGrid import GardenGrid
    from .GridManager import GridManager

class RemoveCommand(ChatCommand):
    name = 'remove'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "remove"

    def execute(self, command_text: str, map: Map, player: HumanPlayer, front_pos : Coord) -> list[Message]:
        messages = []
        carrying_shovel = player.get_state("carrying_shovel")
        if isinstance(carrying_shovel, str):
            removing = map.get_map_objects_at(front_pos)
            for objects in removing:
                if isinstance(objects, ExtDecor):
                    map.remove_from_grid(objects, front_pos)
            messages += map.send_grid_to_players()
            player.set_state("carrying_shovel", 0)
            messages.append(DialogueMessage(self, player, "You have removed the plant!",""))
        else:
            messages.append(DialogueMessage(self, player, "You are not holding a shovel", ""))
        return messages

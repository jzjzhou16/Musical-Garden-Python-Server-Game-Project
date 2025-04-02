from .imports import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from command import ChatCommand
    from maps.base import Map
    from tiles.map_objects import *

class PlantCommand(ChatCommand):
    name = 'plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "plant"

    def execute(self,command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        messages = []
        messages.append(DialogueMessage(self, player, "You activated garden grid!", ""))
        return messages
        

        

from .imports import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from command import ChatCommand
    from maps.base import Map
    from tiles.map_objects import *

class pickUpPlantCommand(ChatCommand):

    name = 'pickup_plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "pickup_plant"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer, plant_name: str) -> list[Message]:
        messages = []
        messages.append(DialogueMessage(self, player, f"You picked up {plant_name}!", ""))
        from .GridManager import GridManager
        note = GridManager.PLANT_NOTES[plant_name.lower()]
        # Default preview note is A2, B2... etc
        sound_message = SoundMessage(player, f"{note}2.mp3", volume = 1.0, repeat = False)
        sound_message_two = SoundMessage(player, f"sound2/{note}2.mp3", volume = 1.0, repeat = False)
        messages.append(sound_message)
        messages.append(sound_message_two)

        return messages
  
class pickUpShovelCommand(ChatCommand):
    name = 'pickup_shovel'
    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "pickup_shovel"
    
    def execute(self, command_text : str, map : Map, player: HumanPlayer, object_name: str) -> list[Message]:
        messages = []
        messages.append(DialogueMessage(self, player, f"You picked up the {object_name}!", ""))
    
        return messages
    
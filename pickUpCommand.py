from .imports import *
from typing import TYPE_CHECKING, List, Optional, Dict
from .PlantAudios import plantAudios


if TYPE_CHECKING:
    from .Plant import Plant
    from command import ChatCommand
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class pickUpPlantCommand(ChatCommand):

    name = 'pickup_plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "pickup_plant"

    def create_sound_message(self, player: "HumanPlayer", plant_name: str) -> SoundMessage: 
        sound_file = plantAudios.get_plant_sound(plant_name)
        return SoundMessage(player, sound_file, volume=0.5, repeat = False) 
    
    def execute(self, command_text : str, map : Map, player: HumanPlayer, plant_name: str) -> list[Message]:
        messages = []
        messages.append(DialogueMessage(self, player, f"You picked up {plant_name}!", ""))
        
        sound_message = self.create_sound_message(player, plant_name)
        messages.append(sound_message)
                
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
    
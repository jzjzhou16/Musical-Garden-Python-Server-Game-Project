from .imports import *
from typing import TYPE_CHECKING, List, Optional, Dict
from .GridCellFactory import GridCellFactory
from .Plant import Plant
from .Plant import PlantFactory
from .PlantAudios import plantAudios

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class pickUpPlantCommand(MenuCommand):

    name = 'pickup_plant'

    def create_sound_message(self, player: "HumanPlayer", plant_name: str) -> SoundMessage: 
        sound_file = plantAudios.get_plant_sound(plant_name)
        return SoundMessage(player, sound_file, volume=0.5) 
    
    def execute(self, context: "Map", player: "HumanPlayer") -> list[Message]:
        messages = []

        player_pos = player.get_current_position()

        # get the objects in the room 
        objects = context.get_objects()

        # Check if the player is standing on a plant 
        for obj, coord in objects:
            if isinstance(obj, Plant) and coord == player_pos:
                plant_name = obj.get_name().replace(".png","") 
                messages.append(DialogueMessage(self, player, f"You picked up {plant_name}!", ""))

                #plant sounds 
                sound_message = self.create_sound_message(player, plant_name)
                messages.append(sound_message)

        return messages

#write a new method in the pick up plant command that returns a sound message where you can append to the message list in execute()

        

from .imports import *
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from command import ChatCommand
    from maps.base import Map
    from tiles.map_objects import *
    from .GardenGrid import GardenGrid
    from .GridManager import GridManager

class PlantCommand(ChatCommand):
    name = 'plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "plant"

    def execute(self, command_text: str, map: Map, player: HumanPlayer, front_pos : Coord) -> list[Message]:
        carrying_plant = player.get_state("carrying_plant")
        carrying_shovel = player.get_state("carrying_shovel")
        messages = []
        
        if isinstance(carrying_plant, str):
            # updates the grid using observer when plant is placed (visual)
            plant_obj = MapObject.get_obj(carrying_plant)
            map.add_to_grid(plant_obj, front_pos)
            
            from .GridManager import GridManager
            manager = GridManager.get_instance()
            if manager:
                # Get plant name in lowercase for note mapping
                plant_name = carrying_plant.lower()
                    
                # Directly call observer method
                manager.on_plant_placed(front_pos.y, front_pos.x, plant_name)

            messages += map.send_grid_to_players()
            # -1 indicating no plants carrying
            player.set_state("carrying_plant", -1)
            messages.append(DialogueMessage(self, player, f"You planted {carrying_plant}!", ""))
            return messages
        elif not isinstance(carrying_shovel, str):
            messages.append(DialogueMessage(self, player, "You are not carrying a plant!", ""))
            return messages
        else:
            messages.append(DialogueMessage(self,player,"There is nothing to remove here.", ""))
            return messages


        
            
        
    
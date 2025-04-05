from .imports import *
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from command import ChatCommand
    from maps.base import Map
    from tiles.map_objects import *

class PlantInteractionCommand(ChatCommand):
    name = 'plant_interaction'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text in ["plant", "remove"]
    
    def _has_plant_at_position(self, map: Map, pos: Coord) -> bool:
        # Helper function to check if there's a plant at given position
        objects = map.get_map_objects_at(pos)
        has_plant = False
        for obj in objects:
            if isinstance(obj, ExtDecor):
                has_plant = True
                break
        return has_plant

    
    def execute(self, command_text: str, map: 'Map', player: 'HumanPlayer') -> List['Message']:
        messages = []
        pos = player.get_current_position()
        front_pos = self._get_position_in_front(pos, player.get_facing_direction())
        if not front_pos:
            messages.append(DialogueMessage(self, player, "There's nothing in front of you!", ""))
            return messages
    
        
        # decide which command to execute based on if there is plant or not
        if self._has_plant_at_position(map, front_pos):
            command = RemoveCommand()
            return command.execute('remove', map, player,front_pos)
        else:
            command = PlantCommand()
            return command.execute('plant', map, player, front_pos)



    def _get_position_in_front(self, pos: Coord, direction: str) -> Optional[Coord]:
        y, x = pos.y, pos.x
        if direction == "up":
            return Coord(y - 1, x)
        elif direction == "down":
            return Coord(y + 1, x)
        elif direction == "left":
            return Coord(y, x - 1)
        elif direction == "right":
            return Coord(y, x + 1)
        return None
    
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
                    from .GridManager import GridManager
                    manager = GridManager.get_instance()
                    if manager:
                    # Get plant name in lowercase for note mapping
                        plant_name = objects.get_name().lower()
                    
                    # Directly call observer method
                        manager.on_plant_removed(front_pos.y, front_pos.x, plant_name)

            messages += map.send_grid_to_players()
            player.set_state("carrying_shovel", 0)
            messages.append(DialogueMessage(self, player, "You have removed the plant!",""))
        else:
            messages.append(DialogueMessage(self, player, "You are not holding a shovel", ""))
        return messages

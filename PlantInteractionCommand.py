from .imports import *
from typing import TYPE_CHECKING, Optional, List
from .RemoveCommand import RemoveCommand
from .PlantCommand import PlantCommand

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
from .imports import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from command import ChatCommand
    from .Plant import PlantFactory, Plant
    from maps.base import Map
    from tiles.map_objects import *

class PlantCommand(ChatCommand):
    name = 'plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "plant"

    def execute(self,command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        carrying_plant = player.get_state("carrying_plant")
        messages = []
        
        if not isinstance(carrying_plant, str):
            messages.append(DialogueMessage(self, player, "You're not carrying a valid plant!", ""))
            return messages
    
        pos = player.get_current_position()
        facing_dir = player.get_facing_direction()
        front_pos = self._get_position_in_front(pos, facing_dir)
        if front_pos:
            map.add_to_grid(MapObject.get_obj(str(carrying_plant)), front_pos)
        messages.append(DialogueMessage(self, player, f"You planted {carrying_plant}!", ""))
        messages += map.send_grid_to_players()
        player.set_state("carrying_plant", 1)
    
        return messages
        
    def _get_position_in_front(self, pos: Coord, direction: str) -> None | Coord:

        y, x = pos.y, pos.x
        if direction == "up":
            return Coord(y - 1, x)
        elif direction == "down":
            return Coord(y + 1, x)
        elif direction == "left":
            return Coord(y, x - 1)
        elif direction == "right":
            return Coord(y, x + 1)

        

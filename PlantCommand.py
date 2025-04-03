from .imports import *
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from command import ChatCommand
    from .Plant import PlantFactory, Plant
    from maps.base import Map
    from tiles.map_objects import *
    from .GardenGrid import GardenGrid
    from .GridManager import GridManager

class PlantCommand(ChatCommand):
    name = 'plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "plant"

    def execute(self, command_text: str, map: Map, player: HumanPlayer) -> list[Message]:
        carrying_plant = player.get_state("carrying_plant")
        messages = []
        
        if not isinstance(carrying_plant, str):
            return [DialogueMessage(self, player, "You're not carrying a valid plant!", "")]
    
        pos = player.get_current_position()
        front_pos = self._get_position_in_front(pos, player.get_facing_direction())
        
        if not front_pos:
            return [DialogueMessage(self, player, "Can't plant here!", "")]
        
        # updates the grid using observer when plant is placed (visual)
        plant_obj = MapObject.get_obj(str(carrying_plant))
        map.add_to_grid(plant_obj, front_pos)
        
        
        # updates the grid using observer when plant is placed (logical)
        from .NPCSingleton import NPCSingleton
        if npc := NPCSingleton._instance:
            grid_row = front_pos.y - 1 
            grid_col = front_pos.x - 1 
                
            if hasattr(npc, 'grid') and hasattr(npc._grid, '_observers'):
                for observer in npc._grid._observers:
                    if hasattr(observer, 'on_plant_placed'):
                        observer.on_plant_placed(grid_row, grid_col, carrying_plant.lower())
            
        return [DialogueMessage(self, player, f"Planted {carrying_plant}!", "")]
            
        
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
from .imports import *
from typing import TYPE_CHECKING
from .GardenGrid import GardenGrid
from .GridCell import GridCell
from .Plant import PlantFactory

if TYPE_CHECKING:
    from command import ChatCommand
    from maps.base import Map
    from tiles.map_objects import *

class PlantCommand(ChatCommand):
    name = 'plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "plant"

    def execute(self, command_text: str, map: "Map", player: HumanPlayer, grid_cell: GridCell) -> list[Message]:
        messages = []
        carrying_plant = player.get_state('carrying_plant', None)
        if not carrying_plant:
            messages.append([DialogueMessage(self, player, "You're not carrying a plant!", "")])
            return messages
        
        player_pos = player.get_current_position()
        grid_origin = grid_cell.get_grid_origin()
        grid_row = player_pos.y - grid_origin.y
        grid_col = player_pos.x - grid_origin.x

        
        
        # Check if the cell isn't empty
        if garden_grid.get_plant(grid_row, grid_col) is not None:
            messages.append(DialogueMessage(self, player, "This spot already has a plant!", ""))
            return messages
        
        # Place the plant
        plant = PlantFactory.get_plant(carrying_plant)
        if plant:
            garden_grid.place_plant(grid_row, grid_col, plant)
            player.set_state('carrying_plant', None)  # Clear carrying state
            messages.append(DialogueMessage(self, player, f"You planted a {carrying_plant}!", ""))
            messages.extend(map.send_grid_to_players())  # Update the grid for all players

        else:
            messages.append(DialogueMessage(self, player, "Failed to plant", ""))

        return messages
        

        

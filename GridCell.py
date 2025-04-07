from .imports import *
from typing import TYPE_CHECKING, List, Optional, Dict
from .plantinteractioncommand import PlantInteractionCommand

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *


class GridCell(MapObject):
    def __init__(self, image_name: str, passable: bool, z_index: int) -> None:
        # Call the MapObject constructor with a fixed image name, passable and z_index
        super().__init__(f'tile/background/{image_name}', passable, z_index)

    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        command = PlantInteractionCommand()
        return command.execute('plant_interaction', player.get_current_room(),player)
    
    def _get_tilemap(self) -> tuple[List[List[MapObject]], int, int]:
        # One cell
        return [[self]], 1, 1

# we need to treat each grid cell as a separate tile for rendering and other actions
# we can use flyweight design so we don't have to create a new mapobject for every cell
#class GridCellFactory:
class GridCellFactory:
    _cells: Dict[str, MapObject] = {}

    def __init__(self, image_name: str):
        self.image_name = image_name

    def get_cell(self, cell_type: str) -> Optional[MapObject]:
        if cell_type not in GridCellFactory._cells:
            # Define the properties for each cell type
            cell_info = {
                "dirt3": {
                    "image_name": self.image_name,  # Use the image name passed during initialization
                    "passable": True,
                    "z_index": 0,
                },
                "dirt":{
                    "image_name": self.image_name,  # Use the image name passed during initialization
                    "passable": True,
                    "z_index": 0,
                }

                # Add more cell types here if needed
            }

            if cell_type in cell_info:
                # Create a new MapObject instance for the cell type
                info = cell_info[cell_type]
                GridCellFactory._cells[cell_type] = GridCell(
                    info["image_name"],
                    passable=info["passable"],
                    z_index=info["z_index"],
                )
            else:
                # Return None if the cell type is not recognized
                return None

        # Return the shared instance
        return GridCellFactory._cells.get(cell_type)
from .imports import *
from .GardenGrid import GardenGrid
from typing import TYPE_CHECKING
from .my_greenhouse_MapObjects import Plant
from .my_greenhouse_MapObjects import PlantFactory


if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class ExampleHouse(Map):
    def __init__(self) -> None:
        self.garden_grid = GardenGrid("cobblestone", grid_rows = 5, grid_cols = 8)
        super().__init__(
            name="Test House",
            description="Welcome to the Musical Garden",
            size=(15, 15),
            entry_point=Coord(14, 7),
            background_tile_image='grass',
        )

        
        
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        # add a door
        door = Door('int_entrance', linked_room="Trottier Town")
        objects.append((door, Coord(14, 7)))

        # add plant shelf
        for plant_name, coord in [("Rose", Coord(7, 13)), ("Tulip", Coord(8, 13)), 
                                  ("Daisy", Coord(9, 13)), ("Sunflower", Coord(10, 13)), 
                                  ("Lilac", Coord(11, 13)), ("Orchid", Coord(12, 13))]:
            plant = PlantFactory.get_plant(plant_name)
            if plant:
                objects.append((plant, coord))

        # Use the persistent garden_grid instance.
        
        objects.append((self.garden_grid, Coord(5, 3)))
        return objects

    def update_player_in_garden(self,player) -> None:
        grid_origin = Coord(5,3)
        grid_columns = self.garden_grid.grid_cols
        grid_rows = self.garden_grid.grid_rows
        
        player_pos = player.get_current_position()

        # Check if player's coordinates are within the garden grid 
        in_garden = (grid_origin.x <= player_pos.x < grid_origin.x + grid_columns and
                     grid_origin.y <= player_pos.y < grid_origin.y + grid_rows)
        
        if in_garden:
            messages = self.garden_grid.player_entered(player)
        
        else:
            messages = self.garden_grid.player_exited(player)

        for msg in messages:
            player.receive_message(msg)
            

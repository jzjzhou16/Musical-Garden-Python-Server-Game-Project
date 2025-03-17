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
        super().__init__(
            name="Test House",
            description="Welcome to the Musical Garden",
            size=(15, 15),
            entry_point=Coord(14, 7),
            background_tile_image='sand',
        )
        self.garden_grid = GardenGrid("cobblestone")
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        # add a door
        door = Door('int_entrance', linked_room="Trottier Town")
        objects.append((door, Coord(14, 7)))

        # add plant shelf
        plant = PlantFactory.get_plant("Rose")
        if plant:
            objects.append((plant, Coord(7, 13)))
        plant = PlantFactory.get_plant("Tulip")
        if plant:
            objects.append((plant, Coord(8, 13)))
        plant = PlantFactory.get_plant("Daisy")
        if plant:
            objects.append((plant, Coord(9, 13)))
        plant = PlantFactory.get_plant("Sunflower")
        if plant:
            objects.append((plant, Coord(10, 13)))
        plant = PlantFactory.get_plant("Lilac")
        if plant:
            objects.append((plant, Coord(11, 13)))
        plant = PlantFactory.get_plant("Orchid")
        if plant:
            objects.append((plant, Coord(12, 13)))

        garden_grid = GardenGrid("cobblestone")
        objects.append((garden_grid, Coord(5, 3)))

        return objects

    def update_player_in_garden(self,player) -> None:
        grid_origin = Coord(5,3)
        grid_columns = self.garden_grid.grid_cols
        grid_rows = self.garden_grid.grid_rows
        
        player_pos = player.get_current.position()

        # Check if player's coordinates are within the garden grid 
        in_garden = (grid_origin.x <= player_pos.x < grid_origin.x + grid_columns and
                     grid_origin.y <= player_pos.y < grid_origin.y + grid_rows)
        
        if in_garden:
            self.garden_grid.player_entered(player)
        
        else:
            self.garden_grid.player_exited(player)
            

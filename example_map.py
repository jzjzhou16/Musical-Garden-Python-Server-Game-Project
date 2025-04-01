from .imports import *
from .GardenGrid import *
from .GridCellFactory import GridCellFactory
from .NPCSingleton import NPCSingleton
from typing import TYPE_CHECKING
from .Plant import Plant, PlantFactory

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *


class ExampleHouse(Map):
    def __init__(self) -> None:
        self.garden_grid = GardenGrid("dirt3", Coord(2,2), 4, 12)
        # constructs NPC Singleton to have one instance of the grid exists at a time
        self.npc = NPCSingleton(
                name="Professor",
                image="prof",
                encounter_text="Welcome to the musical garden!",
                grid=self.garden_grid
            )
        super().__init__(
            name="Test House",
            description="Welcome to the Musical Garden",
            size=(15, 15),
            entry_point=Coord(14, 7),
            background_tile_image='grassBackground',
        )
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        # # add a welcome sign 
        # sign = Sign(text="Welcome to the Musical Greenhouse! Step up to the plant shelf and press SPACE to pick your first plant!.")
        # objects.append((sign, Coord(12, 6)))

        # add a door
        door = Door('int_entrance', linked_room="Trottier Town")
        objects.append((door, Coord(14, 7)))

        # add a tree (decor)
        tree = ExtDecor("tree_large_1") 
        objects.append((tree, Coord(10, 3)))

        # add plant shelf
        for plant_name, coord in [("Rose", Coord(7, 13)), ("Tulip", Coord(8, 13)), 
                                  ("Daisy", Coord(9, 13)), ("Sunflower", Coord(10, 13)), 
                                  ("Lilac", Coord(11, 13)), ("Iris", Coord (12, 13)), ("Orchid", Coord(13, 13))]:
            plant = PlantFactory.get_plant(plant_name)
            if plant:
                objects.append((plant, coord))

         # add npc singleton
        objects.append((self.npc, Coord(1, 1)))

        # add grid cells        
        tilemap, rows, cols = self.garden_grid._get_tilemap()
        grid_origin = self.garden_grid.get_grid_origin()  
        for i in range(rows):
            for j in range(cols):
                cell = tilemap[i][j]
                cell_coord = Coord(grid_origin.y + i, grid_origin.x + j)  
                objects.append((cell, cell_coord))

        return objects


    def move(self, player: HumanPlayer, direction_s: str) -> list[Message]:
        messages = super().move(player, direction_s)
        garden_messages = self.update_player_in_garden(player)
        messages.extend(garden_messages)
        return messages

    
    def update_player_in_garden(self,player:HumanPlayer) -> list[Message]:
        messages = []
        player_pos = player.get_current_position()
        grid_origin = self.garden_grid.get_grid_origin()
        grid_columns = self.garden_grid.grid_cols
        grid_rows = self.garden_grid.grid_rows
        
        # Check if player's coordinates are within the garden grid 
        in_garden = (grid_origin.x <= player_pos.x < grid_origin.x + grid_columns and
                     grid_origin.y <= player_pos.y < grid_origin.y + grid_rows)
        
        if in_garden:
            messages = self.garden_grid.player_entered(player)
        
        else:
            messages = self.garden_grid.player_exited(player)
        
        return messages

        
        
# import pytest

# from ..imports import *
# from ..example_map import ExampleHouse
# from ..GardenGrid import *
# from ..NPCSingleton import *
# from typing import TYPE_CHECKING 

# if TYPE_CHECKING:
#     from coord import Coord
#     from maps.base import Map
#     from tiles.base import MapObject
#     from tiles.map_objects import *

# @pytest.fixture
# def garden_grid():
#     """Create new Mock Garden Grid"""
#     grid = GardenGrid("dirt3", Coord(2, 2), 4, 12)
#     return grid

# def test_singleton():
#     """Test that NPC exhibits singleton behavior (only one instance should exist)"""
#     npc1 = NPCSingleton(
#         name="Professor",
#         image="prof",
#         encounter_text="Welcome!",
#         grid = garden_grid.grid
#     )

#     npc2 = NPCSingleton(
#         name="ShouldNotChange",
#         image="wrong",
#         encounter_text="This shouldn't appear",
#         grid = garden_grid.grid
#     )

#     assert npc1 is npc2  
#     assert npc1.name == "Professor"   
#     assert npc2.name == "Professor"   
#     assert npc1.image == "prof"   


import pytest
from imports import *
from ..NPCSingleton import NPCSingleton
from ..GardenGrid import GardenGrid 

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from maps.base import Map
    from coord import Coord

class NPCSingletonTest:

    @pytest.fixture
    #create new GardenGrid object 
    def garden_grid():
        grid = GardenGrid("dirt3", Coord(2, 2), 4, 12)
        return grid

    @pytest.fixture
    #create new NPC object 
    def npc_instance(garden_grid):
        assert isinstance(garden_grid, GardenGrid), f"Expected GardenGrid, got {type(garden_grid)}"
        return NPCSingleton(
            name="Professor",
            image="prof",
            encounter_text="Welcome to the musical garden!",
            grid=garden_grid
        )
 
    #test that only one instance is being created (singleton!)
    def test_singleton_instance(self, npc_instance, garden_grid) -> None:
        npc2 = NPCSingleton(name="Other NPC", image="other", encounter_text="Another instance?", grid=garden_grid)
        assert npc_instance is npc2, "NPCSingleton should return the same instance every time, as only one exists!"

    #create multiple NPC instances and test singularity across all instances
    def test__multiple_instance_attributes(self, npc_instance, garden_grid) -> None:
        npc2 = NPCSingleton(name="Other NPC", image="other", encounter_text="Another instance?", grid=garden_grid)
        assert npc2.__dict__.get("name") == "Professor", "Singleton should have the same name"
        assert npc2.__dict__.get("image") == "prof", "Singleton should have the same image"
        assert npc2.__dict__.get("encounter_text") == "Welcome to the musical garden!", "Singleton should have the same encounter text"

    #correct coords for NPC
    def test_npc_coord(self, npc_instance) -> None: 
        assert npc_instance.npc_coord == Coord(4, 1), "NPC should start at the correct coordinates"

import pytest
from ..imports import *  
from ..garden_grid import *
from ..grid_cell import GridCell
from ..example_map import ExampleHouse
from ..commands import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import HumanPlayer
    from tiles.map_objects import *

@pytest.fixture
def setup() -> tuple[GridCell,GridCellFactory,HumanPlayer,ExampleHouse]: 
    """test setup"""
    basic_cell = GridCell("dirt3", True, 0)
    factory = GridCellFactory(basic_cell.get_name())
    player = HumanPlayer("test_player") 
    player._current_room = ExampleHouse()
    
    return basic_cell, factory, player, player._current_room

class TestGridCell:
    """Unit Tests for GridCell class - (Flyweight Design Pattern Implementation)"""
    
    def test_grid_cell_initialization(self, setup):
        """Test that GridCell initializes with correct properties"""
        basic_cell, factory, _, _ = setup
        assert basic_cell.get_image_name() == "tile/background/dirt3", "Grid Cell name should reflect the image name "
        assert basic_cell.is_passable() is True, "Grid Cell should be passable"
        assert basic_cell.get_z_index() == 0
        cell_from_factory = factory.get_cell("dirt3")
        assert isinstance(cell_from_factory, GridCell), "Factory should return a GridCell instance"
        assert cell_from_factory.get_image_name() == "tile/background/dirt3", "Factory returned cell should have correct image name"

    def test_grid_cell_flyweight(self, setup):
        """Test that GridCell Factory has the correct flyweight implementation """
        _,factory,_,_ = setup
        cell1_from_factory = factory.get_cell("dirt3")
        cell2_from_factory = factory.get_cell("dirt3")
        cell3_from_factory = factory.get_cell("dirt")
        assert cell1_from_factory == cell2_from_factory, "flyweight object cell 1 and cell 2 should be the same instance"
        assert cell1_from_factory != cell3_from_factory, "flyweight object cell 1 and cell 3 should be separate instances"


    

    def test_player_interaction(self, monkeypatch, setup):
        """Test correct messages returned and player state after interacting with gridcell under 
        different circumstances"""
        def mock_always_has_plant(*args, **kwargs): # Ignore all inputs
            return True
        def mock_never_has_plant(*args, **kwargs): # Ignore all inputs
            return False
    
        test_grid_cell , _, player, _ = setup
    
        # Test case 1: Plant in front but player not carrying shovel
        monkeypatch.setattr(PlantInteractionCommand,'_has_plant_at_position', mock_always_has_plant)
        
        player.set_state("carrying_shovel", 0)
        messages = test_grid_cell.player_interacted(player)
        for msg in messages:
            if isinstance(msg, DialogueMessage):
                message_text = msg._get_data()['dialogue_text']
                break
        assert message_text == "You are not holding a shovel", "Correct message should be displayed"
        

        # Test case 2: Plant in front and player has shovel
        player.set_state("carrying_shovel", "shovel")
        messages = test_grid_cell.player_interacted(player)
        new_state = player.get_state("carrying_shovel")
        for msg in messages:
            if isinstance(msg, DialogueMessage):
                message_text = msg._get_data()['dialogue_text']
                break
        assert message_text == "You have removed the plant!" , "Correct message should be displayed"
        assert new_state == 0, "carrying_shovel state should be 0"

        # Test case 3: No plant in front and player carrying plant
        monkeypatch.setattr(PlantInteractionCommand,'_has_plant_at_position', mock_never_has_plant)
        player.set_state("carrying_plant", "daisy")
        player.set_state("carrying_shovel", 0)
        messages = test_grid_cell.player_interacted(player)
        new_state = player.get_state("carrying_plant")
        for msg in messages:
            if isinstance(msg, DialogueMessage):
                message_text = msg._get_data()['dialogue_text']
                break
        assert message_text == "You planted daisy!", "Correct message should be displayed"
        assert new_state == -1, "carrying_plant state should be -1"


        # Test case 4: No plant in front and player carrying shovel but no plant
        player.set_state("carrying_plant", -1)
        player.set_state("carrying_shovel", "shovel")
        messages = test_grid_cell.player_interacted(player)
        for msg in messages:
            if isinstance(msg, DialogueMessage):
                message_text = msg._get_data()['dialogue_text']
                break
        assert message_text == "There is nothing to remove here.", "Correct message should be displayed"

        
    def test_get_tilemap(self, setup):
        """Test that tilemap representation is correct (visual grid)"""
        basic_cell, _, _, _ = setup
        tilemap, width, height = basic_cell._get_tilemap()
        
        assert len(tilemap) == 1
        assert len(tilemap[0]) == 1
        assert tilemap[0][0] is basic_cell
        assert width == 1
        assert height == 1





import pytest
from ..imports import *  
from ..grid_cell import GridCell, GridCellFactory, GridMessage
from ..example_map import ExampleHouse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer
    from message import Message

@pytest.fixture
def setup(): 
    basic_cell = GridCell("dirt3", True, 0)
    factory = GridCellFactory("tile/background/dirt3")
    player = HumanPlayer("test_player") 
    player._current_room = ExampleHouse()
    return basic_cell, factory, player, player._current_room

class TestGridCell:
    """Unit Tests for GridCell class - (Flyweight Design Pattern Implementation)"""
    
    def test_grid_cell_initialization(self, setup):
        """Test that GridCell initializes with correct properties"""
        basic_cell, _, _, _ = setup
        assert basic_cell.get_image_name() == "tile/background/dirt3"
        assert basic_cell.is_passable() is True
        assert basic_cell.get_z_index() == 0
        
    def test_player_interaction(self, setup):
        """Test that player interaction returns correct messages"""
        basic_cell, _, player, player._current_room = setup
        messages = basic_cell.player_interacted(player)
        
        assert isinstance(messages, list)
        assert all(isinstance(msg, Message) for msg in messages)
        
    def test_get_tilemap(self, setup):
        """Test that tilemap representation is correct (visual grid)"""
        basic_cell, _, _, _ = setup
        tilemap, width, height = basic_cell._get_tilemap()
        
        assert len(tilemap) == 1
        assert len(tilemap[0]) == 1
        assert tilemap[0][0] is basic_cell
        assert width == 1
        assert height == 1





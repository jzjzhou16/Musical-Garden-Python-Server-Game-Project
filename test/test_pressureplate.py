import pytest
from ..pressure_plate import ClearPressurePlate, ColumnPressurePlate
from ..grid_manager import GridManager
from ..imports import *
from ..garden_grid import GardenGrid
from typing import TYPE_CHECKING
from ..example_map import ExampleHouse

if TYPE_CHECKING:
    from message import SoundMessage, DialogueMessage
    from coord import Coord
    from Player import HumanPlayer

@pytest.fixture
def setup():
    """test setup"""
    player = HumanPlayer(name="test player")
    grid = GardenGrid(image_name='dirt', position=Coord(0,0), grid_rows=4, grid_cols=4)
    player._current_room = ExampleHouse()
    manager = GridManager(grid)
    return player, manager

# ColumnPressurePlate tests
def test_column_plate_generates_sounds(setup):
    """Test that correct number of sound messages are generated"""
    player, manager = setup
    plate = ColumnPressurePlate(0)
    
    manager.notes_grid[0][0] = "rose"
    manager.notes_grid[1][0] = "tulip"
    
    messages = plate.player_entered(player)
    
    assert len(messages) == 2
    assert all(isinstance(msg, SoundMessage) for msg in messages)

def test_column_plate_no_sound_when_empty(setup):
    player, manager = setup
    plate = ColumnPressurePlate(1)
    
    messages = plate.player_entered(player)
    assert len(messages) == 0

# ClearPressurePlate tests
def test_clear_plate_removes_plants(setup):
    """Test plants are cleared from grid"""
    player, manager = setup
    plate = ClearPressurePlate()
    
    manager.notes_grid[0][0] = "rose"
    manager.notes_grid[1][1] = "tulip"
    
    messages = plate.player_entered(player)
    
    # grid must be cleared
    assert all(cell is None for row in manager.notes_grid for cell in row)
    assert any(isinstance(msg, DialogueMessage) for msg in messages)

def test_clear_plate_only_clears_once(setup):
    """Test that the clear plate only clears once, then does not affect board"""
    player, manager = setup
    plate = ClearPressurePlate()
    
    messages1 = plate.player_entered(player)
    assert len(messages1) > 0
    
    messages2 = plate.player_entered(player)
    assert len(messages2) == 0
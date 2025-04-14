import pytest
from ..imports import *
from ..garden_grid import GardenGrid
from ..grid_manager import GridManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer

@pytest.fixture
def setup():
    """Basic garden grid fixture"""
    grid = GardenGrid(image_name='dirt', position=Coord(0, 0), grid_rows=4, grid_cols=12)
    grid._observers = []
    manager = GridManager(grid)
    manager.notes_grid = [[None for _ in range(grid.grid_cols)] for _ in range(grid.grid_rows)]
    grid.attach(GridManager(grid))
    return grid, manager

def test_observer_attachment(setup):
    """Verify GridManager is properly attached as observer"""
    grid, manager = setup
    assert len(grid._observers) == 1
    assert manager in grid._observers
    # GridManager implements observer methods
    assert hasattr(manager, 'on_plant_placed')
    assert hasattr(manager, 'on_plant_removed')

def test_plant_notifications(setup):
    """Test plant placement/removal notifications update GridManager"""
    grid, manager = setup
    # placement of plants notification
    grid_row, grid_col = manager._convert_to_grid_coords(1, 2)
    grid.notify_plant_placed(1, 2, "rose")
    grid_row, grid_col = manager._convert_to_grid_coords(1, 2)
    assert manager.notes_grid[grid_row][grid_col] == "rose"
    
    # plant removal notification
    grid.notify_plant_removed(1, 2, "rose")
    assert manager.notes_grid[grid_row][grid_col] is None

def test_player_tracking(setup):
    """Test player entry tracking with GridManager"""
    player = HumanPlayer(name="TestPlayer")
    grid, manager = setup
    
    # Test initial entry
    messages = grid.player_entered(player)
    assert player in grid.players_in_grid
    assert len(messages) == 24  # emotes
    
    # Test exit
    grid.player_exited(player)
    assert player not in grid.players_in_grid

def test_grid_properties(setup):
    """Test grid properties are synchronized"""
    grid, manager = setup
    assert grid.grid_rows == len(manager.notes_grid)
    assert grid.grid_cols == len(manager.notes_grid[0])

def test_full_observer_workflow(setup):
    """Test plant placemtn and removal with GridManager"""
    # plant placement
    grid, manager = setup
    grid.notify_plant_placed(0, 0, "tulip")
    grid_row, grid_col = manager._convert_to_grid_coords(0, 0)
    assert manager.notes_grid[grid_row][grid_col] == "tulip"
    
    # plant removal
    grid.notify_plant_removed(0, 0, "tulip")
    assert manager.notes_grid[grid_row][grid_col] is None
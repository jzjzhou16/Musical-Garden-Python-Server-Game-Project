import pytest
from ..imports import *
from ..garden_grid import GardenGrid
from ..grid_manager import GridManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer

@pytest.fixture
def garden_grid():
    """Basic garden grid fixture"""
    grid = GardenGrid(image_name='dirt', position=Coord(0, 0), grid_rows=4, grid_cols=12)
    grid._observers = []
    return grid

@pytest.fixture
def grid_manager(garden_grid):
    """GridManager fixture properly initialized"""
    manager = GridManager(garden_grid)
    manager.notes_grid = [[None for _ in range(garden_grid.grid_cols)] for _ in range(garden_grid.grid_rows)]
    return manager

def test_observer_attachment(garden_grid, grid_manager):
    """Verify GridManager is properly attached as observer"""
    assert len(garden_grid._observers) == 1
    assert grid_manager in garden_grid._observers
    # Verify GridManager implements observer methods
    assert hasattr(grid_manager, 'on_plant_placed')
    assert hasattr(grid_manager, 'on_plant_removed')

def test_plant_notifications(garden_grid, grid_manager):
    """Test plant placement/removal notifications update GridManager"""
    grid = garden_grid
    # placement of plants notification
    grid_row, grid_col = grid_manager._convert_to_grid_coords(1, 2)
    print(f"Before notify: {grid_manager.notes_grid}")
    grid.notify_plant_placed(3, 3, "rose")
    print(f"After notify: {grid_manager.notes_grid}")
    grid_row, grid_col = grid_manager._convert_to_grid_coords(3, 3)
    assert grid_manager.notes_grid[grid_row][grid_col] == "rose"
    
    # plant removal notification
    garden_grid.notify_plant_removed(1, 2, "rose")
    assert grid_manager.notes_grid[grid_row][grid_col] is None

def test_player_tracking(garden_grid, grid_manager):
    """Test player entry/exit tracking with GridManager"""
    player = HumanPlayer(name="TestPlayer")
    
    # Test initial entry
    messages = garden_grid.player_entered(player)
    assert player in garden_grid.players_in_grid
    assert len(messages) == 24  # emotes
    
    # Test exit
    garden_grid.player_exited(player)
    assert player not in garden_grid.players_in_grid

def test_grid_properties(garden_grid, grid_manager):
    """Test grid properties are synchronized"""
    assert garden_grid.grid_rows == len(grid_manager.notes_grid)
    assert garden_grid.grid_cols == len(grid_manager.notes_grid[0])
    assert garden_grid.get_grid_origin() == grid_manager.grid_origin

def test_full_observer_workflow(garden_grid, grid_manager):
    """Test complete plant lifecycle with GridManager"""
    # Simulate plant placement
    garden_grid.notify_plant_placed(0, 0, "tulip")
    grid_row, grid_col = grid_manager._convert_to_grid_coords(0, 0)
    assert grid_manager.notes_grid[grid_row][grid_col] == "tulip"
    
    # Simulate plant removal
    garden_grid.notify_plant_removed(0, 0, "tulip")
    assert grid_manager.notes_grid[grid_row][grid_col] is None
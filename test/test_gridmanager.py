from typing import TYPE_CHECKING
import pytest
from ..imports import *
from ..grid_manager import GridManager
from ..garden_grid import GardenGrid

if TYPE_CHECKING:
    from coord import Coord

@pytest.fixture
def garden_grid():
    """Basic GardenGrid."""
    return GardenGrid(image_name = 'dirt', position = Coord(1,1), grid_rows=4, grid_cols=4)

@pytest.fixture
def grid_manager(garden_grid):
    """GridManager instance (singleton)."""
    return GridManager(garden_grid)

def test_on_plant_placed(grid_manager, garden_grid):
    """Test that notes_grid updates when a plant is placed."""
    grid_manager.on_plant_placed(row=1, col=1, plant_name="rose")
    grid_row, grid_col = grid_manager._convert_to_grid_coords(1, 1)
    assert grid_manager.notes_grid[grid_row][grid_col] == "rose"

def test_on_plant_removed(grid_manager, garden_grid):
    """Test that notes_grid updates when a plant is removed."""
    grid_manager.on_plant_placed(row=1, col=1, plant_name="tulip")
    grid_manager.on_plant_removed(row=1, col=1, plant_name="tulip")
    grid_row, grid_col = grid_manager._convert_to_grid_coords(1, 1)
    assert grid_manager.notes_grid[grid_row][grid_col] is None

def test_singleton_pattern(garden_grid):
    """Test that only one GridManager instance exists."""
    manager1 = GridManager(garden_grid)
    manager2 = GridManager(garden_grid)
    assert manager1 is manager2
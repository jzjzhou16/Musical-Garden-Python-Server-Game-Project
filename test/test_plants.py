import pytest
from ..imports import *
from ..plants import Plant, PlantFactory

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Player import HumanPlayer


@pytest.fixture
def plant_factory():
    """Fixture to create a PlantFactory instance."""
    return PlantFactory()

def test_plant_creation(plant_factory):
    """Test that a plant can be created."""
    plant = plant_factory.get_plant("rose")
    assert isinstance(plant, Plant), "Factory should return a Plant instance"
    assert plant._image_name == "rose.png", "Factory returned plant should have correct image name"

def test_flyweight_double_add(plant_factory):
    """Test that the flyweight pattern works correctly."""
    factory = PlantFactory()
    plant1 = factory.get_plant("Rose")
    plant2 = factory.get_plant("Rose")
    assert plant1 == plant2, "flyweight object plant 1 and plant 2 should be the same instance"

def test_invalid_plant():
    """Test that an invalid plant name returns None."""
    factory = PlantFactory()
    plant = factory.get_plant("Invalid")
    assert plant is None

def test_image_size():
    """Test that the image size is correct."""
    factory = PlantFactory()
    plant = factory.get_plant("rose")
    if plant is not None:
        assert plant._get_image_size() == (1,1)

def test_player_plants_interaction(plant_factory):
    player = HumanPlayer("test player")
    test_plant = plant_factory.get_plant("rose")
    test_plant2 = plant_factory.get_plant("iris")
    test_plant.player_interacted(player)
    assert player.get_state("carrying_plant") == "rose", "Player's state should reflect the plants that were picked up"
    test_plant2.player_interacted(player)
    assert player.get_state("carrying_plant") == "iris", "Player's state should reflect the plants that were picked up"






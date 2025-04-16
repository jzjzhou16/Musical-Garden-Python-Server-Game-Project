import pytest
from ..imports import *
from ..plants import Plant, PlantFactory
from ..example_map import ExampleHouse

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Player import HumanPlayer
    from message import DialogueMessage


@pytest.fixture
def plant_factory():
    """Fixture to create a PlantFactory instance."""
    return PlantFactory()

@pytest.fixture
def example_setup() -> tuple[Plant, HumanPlayer, ExampleHouse]:
    """test main house setup"""
    plant = Plant("rose")
    player = HumanPlayer("test_player")
    player._current_room = ExampleHouse()
    return plant, player, player._current_room

def test_plant_creation(plant_factory):
    """Test that a plant can be created."""
    plant = plant_factory.get_plant("rose")
    assert isinstance(plant, Plant), "Factory should return a Plant instance"
    assert plant._image_name == "rose", "Factory returned plant should have correct image name"

def test_flyweight_double_add(plant_factory):
    """Test that the flyweight pattern works correctly."""
    factory = PlantFactory()
    plant1 = factory.get_plant("rose")
    plant2 = factory.get_plant("rose")
    assert plant1 == plant2, "flyweight object plant 1 and plant 2 should be the same instance"

def test_image_size():
    """Test that the image size is correct."""
    factory = PlantFactory()
    plant = factory.get_plant("rose")
    if plant is not None:
        assert plant._get_image_size() == (1,1)

def test_player_plants_interaction(example_setup):
    """Test that the player state is correct after interacting with plants."""
    plant,player,example_map = example_setup
    messages = plant.player_interacted(player)
    for msg in messages:
        if isinstance(msg, DialogueMessage):
            message_text = msg._get_data()['dialogue_text']
            break
    assert player.get_state('carrying_plant') == "rose", "Player's state should reflect the plant that were picked up"
    assert message_text == "You picked up rose!", "Messages should be correctly displayed"




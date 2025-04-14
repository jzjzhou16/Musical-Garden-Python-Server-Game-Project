import pytest
from ..imports import *
from ..plants import Plant, PlantFactory


@pytest.fixture
def plant_factory():
    """Fixture to create a PlantFactory instance."""
    return PlantFactory()

def test_plant_creation(plant_factory):
    """Test that a plant can be created."""
    plant = plant_factory.get_plant("rose")
    assert isinstance(plant, Plant)
    assert plant._image_name == "rose.png"

def test_flyweight_double_add():
    """Test that the flyweight pattern works correctly."""
    factory = PlantFactory()
    plant1 = factory.get_plant("Rose")
    plant2 = factory.get_plant("Rose")
    assert plant1 == plant2

def test_invalid_plant():
    """Test that an invalid plant name returns None."""
    factory = PlantFactory()
    plant = factory.get_plant("Invalid")
    assert plant is None

def test_image_size():
    """Test that the image size is correct."""
    factory = PlantFactory()
    plant = factory.get_plant("Rose")
    if plant is not None:
        assert plant._get_image_size() == (1,1)
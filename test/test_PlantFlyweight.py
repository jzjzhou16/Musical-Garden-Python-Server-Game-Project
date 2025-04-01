from imports import *
import pytest
from ..Plant import Plant, PlantFactory
from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

def test_flyweight_two_instances(self):
    """Test that two identical plant instances should be the same"""
    factory = PlantFactory()
    plant1 = factory.get_plant("Rose")
    plant2 = factory.get_plant("Rose")
    assert plant1 == plant2

def test_invalid_plant(self):
    """Test that creating an invalid plant returns None"""
    factory = PlantFactory()
    plant = factory.get_plant("Invalid")
    assert plant is None

def test_image_size(self):
    """Test that  the plant images are the correct size: 1x1"""
    factory = PlantFactory()
    plant = factory.get_plant("Rose")
    if plant is not None:
        assert plant._get_image_size() == (1,1)

def test_all_plant_types(self):
    """Test that all defined plant types can be created"""
    plant_names = ["Daisy", "Lilac", "Orchid", "Rose", "Sunflower", "Tulip"]
    for name in plant_names:
        plant = PlantFactory.get_plant(name)
        assert plant is not None
        assert plant.get_plant_name() == name

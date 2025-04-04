from .imports import *
from typing import TYPE_CHECKING
from typing import Dict, Optional


if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from maps.base import Map

class BackgroundType:
    def __init__(self, image_type: str):
        self.image_type = image_type  

#flyweight factory for background images! 
class BackgroundFactory:
    _instances = {}  

    @classmethod
    def get_background(cls, image_type: str) -> Background:
        if image_type not in cls._instances:
            cls._instances[image_type] = Background(image_type)
        return cls._instances[image_type]
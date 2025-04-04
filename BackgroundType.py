from .imports import *
from typing import TYPE_CHECKING
from typing import List, Dict, Optional
import random


if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from maps.base import Map

class BackgroundType:
    BACKGROUND_OPTIONS: List[str] = [
        'basicGrass',
        'flowerGrass',   
        'plantGrass',
        'stoneGrass',
    ]

    def __init__(self, image_type: str): 
        self.image_type = image_type    

    @classmethod
    def get_random_background_type(cls) -> str: 
        return random.choice(cls.BACKGROUND_OPTIONS)


#flyweight factory for background images! 
class BackgroundFactory:
    _instances = {}  

    @classmethod
    def get_background(cls, image_type: Optional[str] = None) -> Background:
        if image_type is None:
            image_type = BackgroundType.get_random_background_type()

        if image_type not in cls._instances:
            cls._instances[image_type] = Background(image_type)
        return cls._instances[image_type]
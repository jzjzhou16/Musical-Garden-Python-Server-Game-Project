from .imports import *
from typing import TYPE_CHECKING
from typing import List, Optional
import random


if TYPE_CHECKING:
    from tiles.map_objects import *

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
    

class EmoteType:
    EMOTE_OPTIONS: List[str] = ['apple','banana','blueberry','cherry','coconut','greenApple','peach','orange',
                                'lemon','kiwi','horn_02','horn_01','pear','pomegranate','saxophone','strawberry'
    ]
    
    def __init__(self, image_type: str):
        self.image_type = image_type
    @classmethod
    def get_random_emote_type(cls) -> str: 
        return random.choice(cls.EMOTE_OPTIONS)
    



from .imports import *
from typing import TYPE_CHECKING
from typing import List, Optional
import random


if TYPE_CHECKING:
    from tiles.map_objects import *

class BackgroundType:
    """
    A class to represents a map's background tile, with available variations

    Attributes:

    BACKGROUND_OPTIONS: List[str]
        List of available background type names

    """
    BACKGROUND_OPTIONS: List[str] = [
        'basicGrass',
        'flowerGrass',   
        'plantGrass',
        'stoneGrass',
    ]

    def __init__(self, image_type: str): 
        """
        Initializes a BackgroundType instance with a specific image type (from BACKGROUND_OPTIONS)
        
        Parameters:
            image_type (str): The type identifier for the background image
        """
        self.image_type = image_type    

    @classmethod
    def get_random_background_type(cls) -> str: 
        """
        Selects a random background type for each map tile (from BACKGROUND_OPTIONS)

        Parameters:
            cls: the BackgroundType class itself 
        
        Returns:
            (str): The randomly selected background type
        """
        return random.choice(cls.BACKGROUND_OPTIONS)

class BackgroundFactory:
    """
    Flyweight factory: used to manage and resuse various Background instances.
    
    Keeps track of each Background instance to ensure that each background type is only instantiated once, promoting memory efficiency
    
    Attributes:
        _instances: Dictionary that stores created Background instances
    """
    _instances = {}  

    @classmethod
    def get_background(cls, image_type: Optional[str] = None) -> Background:
        """
        Retrieves or creates a Background instance  

        Parameters:
            image_type (Optional[str]): Optional string specifying the background type. If nothing is inputted, a random background tile will be chosen
                        
        Returns:
            cls._instances[image_type]: The specified Background instance
        """

        if image_type is None:  
            image_type = BackgroundType.get_random_background_type()

        if image_type not in cls._instances:
            cls._instances[image_type] = Background(image_type)
        return cls._instances[image_type]

class EmoteType:
    """
    Represents an emote type 
    
    Parameters:
        EMOTE_OPTIONS (List[str]): List of available emote type names
    """

    EMOTE_OPTIONS: List[str] = ['apple','banana','blueberry','cherry','coconut','greenApple','peach','orange',
                                'lemon','kiwi','horn_02','horn_01','pear','pomegranate','saxophone','strawberry'
    ]
    
    def __init__(self, image_type: str):
        """
        Initializes an EmoteType instance with a specific image type
        
        Parameters:
            image_type (str): String that specifies the emote image
        """
        self.image_type = image_type

    @classmethod
    def get_random_emote_type(cls) -> str: 
        """
        Selects a random emote type (from EMOTE_OPTIONS)

        Parameters:
            cls: the EmoteType class itself 
        
        Returns:
            (str): A string representing the randomly selected emote type
        """
        return random.choice(cls.EMOTE_OPTIONS)
    



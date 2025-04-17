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

    def __init__(self, image_type: str) -> None: 
        """
        Initializes a BackgroundType instance with a specific image type (from BACKGROUND_OPTIONS)
        
        Preconditions:
            - image_type must be in BACKGROUND_OPTIONS
        
        Parameters:
            image_type (str): The type identifier for the background image
        """

        #preconditions
        assert image_type in self.BACKGROUND_OPTIONS, f"image_type must be one of {self.BACKGROUND_OPTIONS}"
        self.image_type = image_type    

    @classmethod
    def get_random_background_type(cls) -> str: 
        """
        Selects a random background type for each map tile (from BACKGROUND_OPTIONS)
        
        Preconditions:
            - BACKGROUND_OPTIONS must not be empty

        Parameters:
            cls: the BackgroundType class itself 
        
        Returns:
            (str): The randomly selected background type
        """
        
        #preconditions
        assert len(cls.BACKGROUND_OPTIONS) > 0, "BACKGROUND_OPTIONS cannot be empty"

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

        Preconditions:
            - image_type must exist within BackgroundType.BACKGROUND_OPTIONS

        Parameters:
            image_type (Optional[str]): Optional string specifying the background type. If nothing is inputted, a random background tile will be chosen
                        
        Returns:
            cls._instances[image_type]: The specified Background instance
        """

        #preconditions
        assert image_type in BackgroundType.BACKGROUND_OPTIONS, \
                f"image_type must be one of {BackgroundType.BACKGROUND_OPTIONS}"

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
    
    def __init__(self, image_type: str) -> None:
        """
        Initializes an EmoteType instance with a specific image type
        
        Preconditions:
            - image_type must be in EMOTE_OPTIONS

        Parameters:
            image_type (str): String that specifies the emote image
        """

        #preconditions
        assert image_type in self.EMOTE_OPTIONS, f"image_type must be one of {self.EMOTE_OPTIONS}"

        self.image_type = image_type

    @classmethod
    def get_random_emote_type(cls) -> str: 
        """
        Selects a random emote type (from EMOTE_OPTIONS)

        Preconditions:
            - EMOTE_OPTIONS must not be empty

        Parameters:
            cls: the EmoteType class itself 
        
        Returns:
            (str): A string representing the randomly selected emote type
        """

        #preconditions
        assert len(cls.EMOTE_OPTIONS) > 0, "EMOTE_OPTIONS cannot be empty"
        
        return random.choice(cls.EMOTE_OPTIONS)
    



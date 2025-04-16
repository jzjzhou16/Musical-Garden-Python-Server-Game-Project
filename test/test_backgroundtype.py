import pytest

from ..imports import *
from ..background_type import * 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer

@pytest.fixture
def setup():
    """test setup"""
    factory = BackgroundFactory()
    backgroundOptions = BackgroundType.BACKGROUND_OPTIONS
    random_background = BackgroundType.get_random_background_type()
    emoteOptions = EmoteType.EMOTE_OPTIONS  
    random_emote = EmoteType.get_random_emote_type()
    return backgroundOptions, emoteOptions, factory, random_background, random_emote
 
class TestBackgroundType:
    """Unit Tests for BackgroundType class - (Flyweight Design Pattern Implementation)"""

    def test_background_type_initialization(self, setup):
        """Test that BackgroundType initializes with one of the valid image_type options, for example, basicGrass"""
        backgroundOptions, _, _, _, _ = setup
        background = BackgroundType('basicGrass')
        assert background.image_type == 'basicGrass' 
        assert background.image_type in backgroundOptions

    def test_get_random_background_type(self, setup):
        """Test that random background type is one of the valid options (defined in BACKGROUND_OPTIONS)"""
        backgroundOptions, _, _, random_background, _ = setup
        assert random_background in backgroundOptions
    
class TestBackgroundFactory:
    """Tests main behavior for BackgroundFactory class (Flyweight pattern implementation)"""
    def test_background_factory_initialization(self, setup):
        _, _, factory, _, _ = setup
        assert isinstance(factory, BackgroundFactory)

    def test_background_factory_reuse(self):
        """Test that factory returns same instance for same type"""
        background1 = BackgroundFactory.get_background('basicGrass')
        background2 = BackgroundFactory.get_background('basicGrass')
        assert background1 is background2  # Should be same instance

class TestEmoteType:
    """Tests for EmoteType class"""
    def test_emote_type_initialization(self,setup):
        """Test that EmoteType initializes with one of the valid emote options, for example 'apple'"""
        _, emoteOptions, _, _, _ = setup
        emote = EmoteType('apple')
        assert emote.image_type == 'apple'
        assert emote.image_type in emoteOptions #also test that the image_type is in EMOTE_OPTIONS

    def test_get_random_emote_type(self, setup):
        """Test that random emote type is one of the valid options (defined in EMOTE_OPTIONS)"""
        _, emoteOptions, _, _, random_emote = setup
        assert random_emote in emoteOptions
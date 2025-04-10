import pytest
from ..background_type import Background, BackgroundType, BackgroundFactory, EmoteType
from typing import List
import random

class TestBackgroundType:
    """Unit Tests for BackgroundType class - Pytest"""
    
    def test_background_options(self):
        """Test that BACKGROUND_OPTIONS contains expected values"""
        expected = ['basicGrass', 'flowerGrass', 'plantGrass', 'stoneGrass']
        assert BackgroundType.BACKGROUND_OPTIONS == expected
        
    def test_init_valid_type(self):
        """Test initialization with a valid background type"""
        bg_type = BackgroundType('flowerGrass')
        assert bg_type.image_type == 'flowerGrass'
        
    def test_get_random_type(self, monkeypatch):
        """
        Test that get_random_background_type returns valid option (use lambda to assure the randomization will result in stoneGrass)
        
        Parameters:
            monkeypatch (str): built in pytest feature -> allows for testing with mock variables
        """
        # Dummy random.choice to return predictable value
        monkeypatch.setattr(random, 'choice', lambda x: 'stoneGrass')
        result = BackgroundType.get_random_background_type()
        assert result in BackgroundType.BACKGROUND_OPTIONS
        assert result == 'stoneGrass'

class TestBackgroundFactory:
    """Tests for BackgroundFactory class help"""

class TestEmoteType:
    """Tests for EmoteType class"""
    
    def test_emote_options(self):
        """Test that EMOTE_OPTIONS contains expected values"""
        expected = ['apple','banana','blueberry','cherry','coconut',
                   'greenApple','peach','orange','lemon','kiwi',
                   'horn_02','horn_01','pear','pomegranate',
                   'saxophone','strawberry']
        assert EmoteType.EMOTE_OPTIONS == expected
        
    def test_init(self):
        """Test initialization with a valid emote type"""
        emote = EmoteType('apple')
        assert emote.image_type == 'apple'
        
    def test_get_random_emote(self, monkeypatch):
        """
        Test that get_random_emote_type returns valid option

        Parameters:
            monkeypatch (str): built in pytest feature -> allows for testing with mock variables
        """
        monkeypatch.setattr(random, 'choice', lambda x: 'saxophone')
        result = EmoteType.get_random_emote_type()
        assert result in EmoteType.EMOTE_OPTIONS
        assert result == 'saxophone'
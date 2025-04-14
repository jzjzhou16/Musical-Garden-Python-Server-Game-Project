import pytest

from ..imports import *  
from ..buttons import Shovel, PlayButton1, PlayButton2, PlayButton3
from ..commands import pickUpShovelCommand, happybirthdayCommand, twinkleCommand, jingleBellsCommand
from ..example_map import ExampleHouse
from ..demo_room import DemoRoom

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer
    from message import Message

@pytest.fixture
def setup():
    shovel = Shovel("Shovel")
    play_button1 = PlayButton1("playButton")
    play_button2 = PlayButton2("playButton")
    play_button3 = PlayButton3("playButton")
    player = HumanPlayer("test_player")
    player._current_room = DemoRoom()
    player._current_room = ExampleHouse()
    return shovel, play_button1, play_button2, play_button3, player, player._current_room, player._current_room

class TestShovel:
    """Tests for Shovel button class"""
    
    def test_shovel_initialization(self, setup):
        """Test that Shovel initializes with correct image"""
        shovel, _, _, _, _, _, _ = setup
        assert shovel._Shovel__image == "Shovel"
        
    def test_shovel_interaction(self, setup):
        """Test that shovel interaction sets player state correctly and returns the right messages"""
        shovel, _, _, _, player, _, player._current_room = setup
        messages = shovel.player_interacted(player)
        
        assert player.get_state('carrying_shovel') == "Shovel"
        assert isinstance(messages, list)
        assert all(isinstance(msg, Message) for msg in messages)

class TestPlayButton1:
    """Tests for PlayButton1 (happy birthday button)"""
    
    def test_playbutton1_initialization(self, setup):
        """Test that PlayButton1 initializes with correct image"""
        _, button, _, _, _, _, _= setup
        assert button._PlayButton1__image == "playButton"
        
    def test_playbutton1_interaction(self, setup):
        """Test that button interaction returns the correct soundMessage/messages"""
        _, button, _, _, player, player._current_room, _ = setup
        messages = button.player_interacted(player) 
        
        assert isinstance(messages, list)
        assert all(isinstance(msg, Message) for msg in messages)

class TestPlayButton2:
    """Tests for PlayButton2 (twinkle button)"""
    
    def test_playbutton2_initialization(self, setup):
        """Test that PlayButton2 initializes with correct image"""
        _, _, button, _, _, _, _ = setup
        assert button._PlayButton2__image == "playButton"
        
    def test_playbutton2_interaction(self, setup):
        """Test that button interaction returns the correct soundMessage/messages"""
        _, button, _, _, player, player._current_room, _ = setup
        messages = button.player_interacted(player) 
        
        assert isinstance(messages, list)
        assert all(isinstance(msg, Message) for msg in messages)

class TestPlayButton3:
    """Tests for PlayButton3 (jingle bells button)"""
    
    def test_playbutton3_initialization(self, setup):
        """Test that PlayButton3 initializes with correct image"""
        _, _, _, button, _, _, _ = setup
        assert button._PlayButton3__image == "playButton"
        
    def test_playbutton3_interaction(self, setup):
        """Test that button interaction returns the correct soundMessage/messages"""
        _, button, _, _, player, player._current_room, _ = setup
        messages = button.player_interacted(player)
        
        assert isinstance(messages, list)
        assert all(isinstance(msg, Message) for msg in messages)
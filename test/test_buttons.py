import pytest

from ..imports import *  
from ..buttons import Shovel, PlayButton1, PlayButton2, PlayButton3
from ..example_map import ExampleHouse
from ..demo_room import DemoRoom

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer
    from message import *

@pytest.fixture
def demo_setup() -> tuple[PlayButton1,PlayButton2,PlayButton3,HumanPlayer,DemoRoom]:
    """test demo room setup"""
    play_button1 = PlayButton1("playButton")
    play_button2 = PlayButton2("playButton")
    play_button3 = PlayButton3("playButton")
    player = HumanPlayer("test_player")
    player._current_room = DemoRoom()
    return play_button1, play_button2, play_button3, player, player._current_room

@pytest.fixture 
def example_setup() -> tuple[Shovel, HumanPlayer, ExampleHouse]:
    """test main house setup"""
    shovel = Shovel("Shovel")
    player = HumanPlayer("test_player")
    player._current_room = ExampleHouse()
    return shovel, player, player._current_room


class TestPlayButton1:
    """Tests for PlayButton1 (happy birthday button)"""
    
    def test_playbutton1_initialization(self, demo_setup):
        """Test that PlayButton1 initializes with correct image"""
        play_button1, _, _, _, _= demo_setup
        assert play_button1._PlayButton1__image == "playButton",  "Play button 1 should have the right image"
        
    def test_playbutton1_interaction(self, demo_setup):
        """Test that button interaction returns the correct soundMessage/DialogueMessage"""
        play_button1, _, _, player, demo_room = demo_setup
        messages = play_button1.player_interacted(player) 
        for msg in messages:
            if isinstance(msg, DialogueMessage):
                message_text = msg._get_data()['dialogue_text']
                break
        
        assert message_text == "Here is the demo for 'Happy Birthday'!", "Messages should be correctly displayed"

class TestPlayButton2:
    """Tests for PlayButton2 (twinkle button)"""
    
    def test_playbutton2_initialization(self, demo_setup):
        """Test that PlayButton2 initializes with correct image"""
        _, play_button2, _, _, _= demo_setup
        assert play_button2._PlayButton2__image == "playButton", "Play button 2 should have the right image"
        
    def test_playbutton2_interaction(self, demo_setup):
        """Test that button interaction returns the correct soundMessage/messages"""
        _, play_button2, _, player, demo_room = demo_setup
        messages = play_button2.player_interacted(player) 
        for msg in messages:
            if isinstance(msg, DialogueMessage):
                message_text = msg._get_data()['dialogue_text']
                break
    
        assert message_text == "Here is the demo for 'Twinkle Twinkle Little Stars'!", "Messages should be correctly displayed"

class TestPlayButton3:
    """Tests for PlayButton3 (jingle bells button)"""
    
    def test_playbutton3_initialization(self, demo_setup):
        """Test that PlayButton3 initializes with correct image"""
        _, _, play_button3, _, _ = demo_setup
        assert play_button3._PlayButton3__image == "playButton", "Play button 3 should have the right image"
        
    def test_playbutton3_interaction(self, demo_setup):
        """Test that button interaction returns the correct soundMessage/messages"""
        _, _, play_button3, player, demo_room= demo_setup
        messages = play_button3.player_interacted(player)
        for msg in messages:
            if isinstance(msg, DialogueMessage):
                message_text = msg._get_data()['dialogue_text']
                break

        assert message_text == "Here is the demo for 'Jingle Bells'!", "Messages should be correctly displayed"


class TestShovel:
    """Tests for Shovel button class"""
    
    def test_shovel_initialization(self, example_setup):
        """Test that Shovel initializes with correct image"""
        shovel, _, _ = example_setup
        assert shovel._Shovel__image == "Shovel", "Shovel should have the right image"
        
    def test_shovel_interaction(self, example_setup):
        """Test that pick up shovel interaction sets player state correctly and returns the right messages"""
        shovel,player,example_map = example_setup
        messages = shovel.player_interacted(player)
        for msg in messages:
            if isinstance(msg, DialogueMessage):
                message_text = msg._get_data()['dialogue_text']
                break
        assert player.get_state('carrying_shovel') == "Shovel", "Player's state should reflect the shovel that were picked up"
        assert message_text == "You picked up the Shovel!", "Messages should be correctly displayed"


from .imports import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from command import ChatCommand
    from maps.base import Map
    from tiles.map_objects import *


class happybirthdayCommand(ChatCommand):

    name = 'happy_birthday'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "happy_birthday"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        messages = []
          
        demo_happybirthay = {
            Coord(3, 1): "Daisy",  # C
            Coord(3, 2): "Daisy",  # C
            Coord(3, 3): "Sunflower", #D
            Coord(3, 4): "Daisy",  # C
            Coord(3, 5): "Lilac",   # F
            Coord(3, 6): "Iris",   # E   
            Coord(3, 7): "Daisy",  # C
            Coord(3, 8): "Daisy",  # C
            Coord(3, 9): "Sunflower",# D
            Coord(3, 10): "Daisy",  # C
            Coord(3, 11): "Orchid",   # G
            Coord(3, 12): "Lilac", #F
           }  
        
        for coord, plant_name in demo_happybirthay.items():
            plant_obj = MapObject.get_obj(plant_name)
            map.add_to_grid(plant_obj, coord)
        messages += map.send_grid_to_players()
        messages.append(SoundMessage(player, f"happy_birthday.mp3", volume = 0.1, repeat = False))
        # Adding a second folder with duplicates to allow two sounds to play with different paths (treated separately)
        # messages.append(SoundMessage(player, f"sound2/happy_birthday.mp3",volume=1.0,repeat=False))
        messages.append(DialogueMessage(self, player, "Here is the demo for 'Happy Birthday'!", ""))

        return messages
            

class twinkleCommand(ChatCommand):

    name = 'twinkle'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "twinkle"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        messages = []


        demo_twinkle = { 
            Coord(8, 1): "Daisy",   # C
            Coord(8, 2): "Daisy",   # C
            Coord(8, 3): "Orchid",  # G
            Coord(8, 4): "Orchid",  # G
            Coord(9, 5): "Rose",   # A
            Coord(9, 6): "Rose",   # A
            Coord(8, 7): "Orchid", # G
           } 
        for coord, plant_name in demo_twinkle.items():
            plant_obj = MapObject.get_obj(plant_name)
            map.add_to_grid(plant_obj, coord)

        messages += map.send_grid_to_players()
        messages.append(SoundMessage(player, f"twinkle_twinkle.mp3", volume = 1.0, repeat = False))
        # Adding a second folder with duplicates to allow two sounds to play with different paths (treated separately)
        # messages.append(SoundMessage(player, f"sound2/twinkle_twinkle.mp3",volume=1.0,repeat=False))
        messages.append(DialogueMessage(self, player, "Here is the demo for 'Twinkle Twinkle Little Star'!", ""))
        
        return messages
            
class jingleBellsCommand(ChatCommand):

    name = 'jingle_bells'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "jingle_bells"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        messages = []
        
        demo_jingle = {
            Coord(15, 1): "Iris",     # E
            Coord(15, 2): "Iris",     # E
            Coord(15, 3): "Iris",     # E
            Coord(15, 4): "Iris",     # E
            Coord(15, 5): "Iris",     # E
            Coord(15, 6): "Iris",     # E
            Coord(15, 7): "Iris",     # E 
            Coord(15, 8): "Orchid",   # G
            Coord(15, 9): "Daisy",     # C 
            Coord(15, 10): "Sunflower", # D
            Coord(15, 11): "Iris",    # E
           }  
        for coord, plant_name in demo_jingle.items():
            plant_obj = MapObject.get_obj(plant_name)
            map.add_to_grid(plant_obj, coord)

        messages += map.send_grid_to_players()
        messages.append(SoundMessage(player, f"jingle_bells.mp3", volume = 1.0, repeat = False))
        # Adding a second folder with duplicates to allow two sounds to play with different paths (treated separately)
        # messages.append(SoundMessage(player, f"sound2/jingle_bells.mp3",volume=1.0,repeat=False))
        messages.append(DialogueMessage(self, player, "Here is the demo for 'Jingle Bells'!", ""))
        return messages

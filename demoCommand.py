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
        removing = map.get_objects()
        for objects in removing:
            if isinstance(objects, ExtDecor):
                map.remove_from_grid(objects, objects.get_position())
                from .GridManager import GridManager
                manager = GridManager.get_instance()
                if manager:
                # Get plant name in lowercase for note mapping
                    plant_name = objects.get_name().lower()
                    
                # Directly call observer method
                    manager.on_plant_removed(objects.get_position().y, objects.get_position().x, plant_name)

        messages += map.send_grid_to_players()

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

            from.GridManager import GridManager
            manager = GridManager.get_instance()
            if manager:
                # Get plant name in lowercase for note mapping
                name = plant_name.lower()
            

                    
                # Directly call observer method
                manager.on_plant_placed(coord.y, coord.x, name)

            messages += map.send_grid_to_players()
        messages.append(DialogueMessage(self, player, "Here is the demo for 'Happy Birthday'!", ""))
        return messages
            

class twinkleCommand(ChatCommand):

    name = 'twinkle'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "twinkle"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        messages = []

        removing = map.get_objects()
        for objects in removing:
            if isinstance(objects, ExtDecor):
                map.remove_from_grid(objects, objects.get_position())
                from .GridManager import GridManager
                manager = GridManager.get_instance()
                if manager:
                # Get plant name in lowercase for note mapping
                    plant_name = objects.get_name().lower()
                    
                # Directly call observer method
                    manager.on_plant_removed(objects.get_position().y, objects.get_position().x, plant_name)

        messages += map.send_grid_to_players()



        demo_twinkle = {
            # Coord(10, 1): "Rose",    # A 
            # Coord(10, 3): "Orchid",  # G
            # Coord(10, 4): "Orchid",  # G 
            Coord(3, 1): "Daisy",   # C
            Coord(3, 2): "Daisy",   # C
            Coord(3, 3): "Orchid",  # G
            Coord(3, 4): "Orchid",  # G
            Coord(4, 5): "Rose",   # A
            Coord(4, 6): "Rose",   # A
            Coord(3, 7): "Orchid", # G
           }  
        for coord, plant_name in demo_twinkle.items():
            plant_obj = MapObject.get_obj(plant_name)
            map.add_to_grid(plant_obj, coord)

            from.GridManager import GridManager
            manager = GridManager.get_instance()
            if manager:
                # Get plant name in lowercase for note mapping
                name = plant_name.lower()
                    
                # Directly call observer method
                manager.on_plant_placed(coord.y, coord.x, name)

            messages += map.send_grid_to_players()
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
            Coord(3, 1): "Iris",     # E
            Coord(3, 2): "Iris",     # E
            Coord(3, 3): "Iris",     # E
            Coord(3, 4): "Iris",     # E
            Coord(3, 6): "Iris",     # E
            Coord(3, 7): "Iris",     # E
            Coord(3, 8): "Iris",     # E 
            Coord(3, 9): "Orchid",   # G
            Coord(3, 10): "Daisy",     # C 
            Coord(3, 11): "Sunflower", # D
            Coord(3, 12): "Iris",    # E
           }  
        for coord, plant_name in demo_jingle.items():
            plant_obj = MapObject.get_obj(plant_name)
            map.add_to_grid(plant_obj, coord)

            from.GridManager import GridManager
            manager = GridManager.get_instance()
            if manager:
                # Get plant name in lowercase for note mapping
                name = plant_name.lower()
                    
                # Directly call observer method
                manager.on_plant_placed(coord.y, coord.x, name)

            messages += map.send_grid_to_players()
        messages.append(DialogueMessage(self, player, "Here is the demo for 'Jingle Bells'!", ""))
        return messages


from .imports import *
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from command import ChatCommand
    from maps.base import Map
    from tiles.map_objects import *

#plant_interaction_command
class PlantInteractionCommand(ChatCommand):
    name = 'plant_interaction'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text in ["plant", "remove"]
    
    def _has_plant_at_position(self, map: Map, pos: Coord) -> bool:
        # Helper function to check if there's a plant at given position
        objects = map.get_map_objects_at(pos)
        has_plant = False
        for obj in objects:
            if isinstance(obj, ExtDecor):
                has_plant = True
                break
        return has_plant

    
    def execute(self, command_text: str, map: 'Map', player: 'HumanPlayer') -> List['Message']:
        messages = []
        pos = player.get_current_position()
        front_pos = self._get_position_in_front(pos, player.get_facing_direction())
        if not front_pos:
            messages.append(DialogueMessage(self, player, "There's nothing in front of you!", ""))
            return messages
    
        
        # decide which command to execute based on if there is plant or not
        if self._has_plant_at_position(map, front_pos):
            command = RemoveCommand()
            return command.execute('remove', map, player,front_pos)
        else:
            command = PlantCommand()
            return command.execute('plant', map, player, front_pos)



    def _get_position_in_front(self, pos: Coord, direction: str) -> Optional[Coord]:
        y, x = pos.y, pos.x
        if direction == "up":
            return Coord(y - 1, x)
        elif direction == "down":
            return Coord(y + 1, x)
        elif direction == "left":
            return Coord(y, x - 1)
        elif direction == "right":
            return Coord(y, x + 1)
        return None
    
class PlantCommand(ChatCommand):
    name = 'plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "plant"

    def execute(self, command_text: str, map: Map, player: HumanPlayer, front_pos : Coord) -> list[Message]:
        carrying_plant = player.get_state("carrying_plant")
        carrying_shovel = player.get_state("carrying_shovel")
        messages = []
        
        if isinstance(carrying_plant, str):
            # updates the grid using observer when plant is placed (visual)
            plant_obj = MapObject.get_obj(carrying_plant)
            map.add_to_grid(plant_obj, front_pos)
            
            from .grid_manager import GridManager
            manager = GridManager.get_instance()
            if manager:
                # Get plant name in lowercase for note mapping
                plant_name = carrying_plant.lower()
                    
                # Directly call observer method
                manager.on_plant_placed(front_pos.y, front_pos.x, plant_name)

            messages += map.send_grid_to_players()
            # -1 indicating no plants carrying
            player.set_state("carrying_plant", -1)
            messages.append(DialogueMessage(self, player, f"You planted {carrying_plant}!", ""))
            return messages
        elif not isinstance(carrying_shovel, str):
            messages.append(DialogueMessage(self, player, "You are not carrying a plant!", ""))
            return messages
        else:
            messages.append(DialogueMessage(self,player,"There is nothing to remove here.", ""))
            return messages


        
class RemoveCommand(ChatCommand):
    name = 'remove'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "remove"

    def execute(self, command_text: str, map: Map, player: HumanPlayer, front_pos : Coord) -> list[Message]:
        messages = []
        carrying_shovel = player.get_state("carrying_shovel")
        if isinstance(carrying_shovel, str):
            removing = map.get_map_objects_at(front_pos)
            for objects in removing:
                if isinstance(objects, ExtDecor):
                    map.remove_from_grid(objects, front_pos)
                    from .grid_manager import GridManager
                    manager = GridManager.get_instance()
                    if manager:
                    # Get plant name in lowercase for note mapping
                        plant_name = objects.get_name().lower()
                    
                    # Directly call observer method
                        manager.on_plant_removed(front_pos.y, front_pos.x, plant_name)

            messages += map.send_grid_to_players()
            player.set_state("carrying_shovel", 0)
            messages.append(DialogueMessage(self, player, "You have removed the plant!",""))
        else:
            messages.append(DialogueMessage(self, player, "You are not holding a shovel", ""))
        return messages

#pickup_command
class pickUpPlantCommand(ChatCommand):

    name = 'pickup_plant'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "pickup_plant"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer, plant_name: str) -> list[Message]:
        messages = []
        messages.append(DialogueMessage(self, player, f"You picked up {plant_name}!", ""))
        from .grid_manager import GridManager
        note = GridManager.PLANT_NOTES[plant_name.lower()]
        # Default preview note is A2, B2... etc
        messages.append(SoundMessage(player, f"{note}_2.mp3", volume = 1.0, repeat = False))
        messages.append(SoundMessage(player, f"sound2/{note}.mp3", volume = 1.0, repeat = False))

        return messages
  
class pickUpShovelCommand(ChatCommand):
    name = 'pickup_shovel'
    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == "pickup_shovel"
    
    def execute(self, command_text : str, map : Map, player: HumanPlayer, object_name: str) -> list[Message]:
        messages = []
        messages.append(DialogueMessage(self, player, f"You picked up the {object_name}!", ""))
    
        return messages
    
#demo room commands

class happybirthdayCommand(ChatCommand):
    """
    Chat command that plays the Happy Birthday Demo 
    
    Places plants in a pre-defined pattern that plays the Happy Birthday melody when activated.
    Inherits from ChatCommand to implement the Command Design Pattern
    
    Parameters:
        name (str): The command name ('happy_birthday')
    """

    name = 'happy_birthday'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        """
        Determines if the input text matches the command
        
        Parameter:
            command_text (str): The text input to check against the command
            
        Returns:
            (bool): True if the input matches the command's name. False otherwise.
        """
        return command_text == "happy_birthday"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        """
        Executes the Happy Birthday demo command
        
        Parameters:
            command_text (str): The String that triggers the command execution 
            map (Map): The game map where plants will be placed 
            player (HumanPlayer): The player who triggers the command
            
        Returns:
            list[Message]: Messages containing:
                - updates to grid showing the new plant arrangement
                - happy birthday audio file 
                - dialogue confirmation
        """
        messages = []
          
        demo_happybirthay = {
            Coord(3, 1): "daisy",  # C
            Coord(3, 2): "daisy",  # C
            Coord(3, 3): "sunflower", #D
            Coord(3, 4): "daisy",  # C
            Coord(3, 5): "lilac",   # F
            Coord(3, 6): "iris",   # E   
            Coord(3, 7): "daisy",  # C
            Coord(3, 8): "daisy",  # C
            Coord(3, 9): "sunflower",# D
            Coord(3, 10): "daisy",  # C
            Coord(3, 11): "orchid",   # G
            Coord(3, 12): "lilac", #F
           }  
        
        for coord, plant_name in demo_happybirthay.items():
            plant_obj = MapObject.get_obj(plant_name)
            map.add_to_grid(plant_obj, coord)
        messages += map.send_grid_to_players()
        messages.append(SoundMessage(player, f"happy_birthday.mp3", volume = 1.0, repeat = False))
        # Adding a second folder with duplicates to allow two sounds to play with different paths (treated separately)
        # messages.append(SoundMessage(player, f"sound2/happy_birthday.mp3",volume=1.0,repeat=False))
        messages.append(DialogueMessage(self, player, "Here is the demo for 'Happy Birthday'!", ""))

        return messages
            

class twinkleCommand(ChatCommand):
    """
    Chat command that plays the Twinkle Twinkle Little Star Demo 
    
    Places plants in a pre-defined pattern that plays the Twinkle Twinkle Little Star melody when activated.
    Inherits from ChatCommand to implement the Command Design Pattern
    
    Parameters:
        name (str): The command name ('twinkle')
    """

    name = 'twinkle'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        """
        Determines if the input text matches the command
        
        Parameter:
            command_text (str): The text input to check against the command
            
        Returns:
            (bool): True if the input matches the command's name. False otherwise.
        """
        return command_text == "twinkle"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        """
        Executes the Twinkle Twinkle Little Star demo command
        
        Parameters:
            command_text (str): The String that triggers the command execution 
            map (Map): The game map where plants will be placed 
            player (HumanPlayer): The player who triggers the command
            
        Returns:
            list[Message]: Messages containing:
                - updates to grid showing the new plant arrangement
                - twinkle twinkle tittle star audio file 
                - dialogue confirmation
        """
        
        messages = []


        demo_twinkle = { 
            Coord(8, 1): "daisy",   # C
            Coord(8, 2): "daisy",   # C
            Coord(8, 3): "orchid",  # G
            Coord(8, 4): "orchid",  # G
            Coord(9, 5): "rose",   # A
            Coord(9, 6): "rose",   # A
            Coord(8, 7): "orchid", # G
           } 
        for coord, plant_name in demo_twinkle.items():
            plant_obj = MapObject.get_obj(plant_name)
            map.add_to_grid(plant_obj, coord)

        messages += map.send_grid_to_players()
        messages.append(SoundMessage(player, f"twinkle_twinkle.mp3", volume = 1.0, repeat = False))
        messages.append(DialogueMessage(self, player, "Here is the demo for 'Twinkle Twinkle Little Star'!", ""))
        
        return messages
            
class jingleBellsCommand(ChatCommand):
    """
    Chat command that plays the Jingle Bells Demo 
    
    Places plants in a pre-defined pattern that plays the Jingle Bells melody when activated.
    Inherits from ChatCommand to implement the Command Design Pattern
    
    Parameters:
        name (str): The command name ('jingle_bells')
    """

    name = 'jingle_bells'

    @classmethod
    def matches(cls, command_text: str) -> bool:
        """
        Determines if the input text matches the command
        
        Parameter:
            command_text (str): The text input to check against the command
            
        Returns:
            (bool): True if the input matches the command's name. False otherwise.
        """
        return command_text == "jingle_bells"

    
    def execute(self, command_text : str, map : Map, player: HumanPlayer) -> list[Message]:
        """
        Executes the Jingle Bells demo command
        
        Parameters:
            command_text (str): The String that triggers the command execution 
            map (Map): The game map where plants will be placed 
            player (HumanPlayer): The player who triggers the command
            
        Returns:
            list[Message]: Messages containing:
                - updates to grid showing the new plant arrangement
                - jingle bells audio file 
                - dialogue confirmation
        """

        messages = []
        
        demo_jingle = {
            Coord(15, 1): "iris",     # E
            Coord(15, 2): "iris",     # E
            Coord(15, 3): "iris",     # E
            Coord(15, 4): "iris",     # E
            Coord(15, 5): "iris",     # E
            Coord(15, 6): "iris",     # E
            Coord(15, 7): "iris",     # E 
            Coord(15, 8): "orchid",   # G
            Coord(15, 9): "daisy",     # C 
            Coord(15, 10): "sunflower", # D
            Coord(15, 11): "iris",    # E
           }  
        for coord, plant_name in demo_jingle.items():
            plant_obj = MapObject.get_obj(plant_name)
            map.add_to_grid(plant_obj, coord)

        messages += map.send_grid_to_players()
        messages.append(SoundMessage(player, f"jingle_bells.mp3", volume = 1.0, repeat = False))
        messages.append(DialogueMessage(self, player, "Here is the demo for 'Jingle Bells'!", ""))
        return messages

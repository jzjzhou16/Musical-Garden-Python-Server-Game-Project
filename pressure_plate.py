from .imports import *
from typing import TYPE_CHECKING, List
from .grid_manager import GridManager

if TYPE_CHECKING:
    from message import Message, SoundMessage
    from grid_manager import GridManager
    from tiles.map_objects import *

class ColumnPressurePlate(PressurePlate):
    def __init__(self, column_index: int):
        super().__init__(image_name='musicNote', stepping_text='')
        self.__active = False
        self.column_index = column_index

    def player_entered(self, player) -> List['SoundMessage']:
        messages = []
        
        if not self.__active:
            self.__active = True
            manager = GridManager.get_instance()
            
            if not manager:
                return messages
            
            for row in range(4):
                plant_name = manager.notes_grid[row][self.column_index]
                if plant_name and plant_name in GridManager.PLANT_NOTES:
                    note = GridManager.PLANT_NOTES[plant_name]
                    octave = GridManager.ROW_OCTAVES[row]
                    messages.append(SoundMessage(
                        player,
                        f"{note}_{octave}.mp3",
                        volume=1.0,
                        repeat=False
                    ))
                    # Adding a second folder with duplicates to allow two sounds to play with different paths (treated separately)
        
        return messages
    
    def player_exited(self, player) -> List['Message']:
        self.__active = False
        return []
    

class ClearPressurePlate(PressurePlate):
    def __init__(self):
        super().__init__(image_name='delete', stepping_text='Cleared all plants from the board')
        self.__active = False
        
    def player_entered(self, player) -> List['Message']:
        messages = []
        if not self.__active:
            self.__active = True
            manager = GridManager.get_instance()
            
            if not manager:
                return messages
            # clears all plants in grid visually and on logical grid (in grid manager)
            messages.extend(manager.clear_all_plants(player.get_current_room()))
            # display message to player
            messages.append(DialogueMessage(self, player, "Cleared all plants from the board", ""))

        return messages
    
    def player_exited(self, player) -> List['Message']:
        self.__active = False
        return []
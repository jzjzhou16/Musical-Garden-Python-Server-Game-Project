from .imports import *
from typing import TYPE_CHECKING, List
from .GridManager import GridManager

if TYPE_CHECKING:
    from message import Message, SoundMessage
    from GridManager import GridManager
    from tiles.map_objects import PressurePlate

class ColumnPressurePlate(PressurePlate):
    def __init__(self, column_index: int):
        super().__init__(image_name='pressure_plate', stepping_text='')
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
                if plant_name and plant_name.lower() in GridManager.PLANT_NOTES:
                    note = GridManager.PLANT_NOTES[plant_name.lower()]
                    octave = GridManager.ROW_OCTAVES[row]
                    messages.append(SoundMessage(
                        player,
                        f"{note}{octave}.mp3",
                        volume=0.7,
                        repeat=False
                    ))
        
        return messages

    def player_exited(self, player) -> List['Message']:
        self.__active = False
        return []
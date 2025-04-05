from .imports import *
from typing import TYPE_CHECKING, List
from .GridManager import GridManager
from .Observer import PlantObserver

if TYPE_CHECKING:
    from Player import HumanPlayer
    from message import Message, DialogueMessage, SoundMessage
    from GridManager import GridManager
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import UtilityObject
    from tiles.map_objects import Observer

class ColumnPressurePlate(UtilityObject):
    def __init__(self, column_index: int):
        super().__init__(f"pressure_plate", passable=True)
        self.__active = False
        self.column_index = column_index

    def update(self) -> List[Message]:
        return []

    def player_entered(self, player) -> List[SoundMessage]:
        if not self.__active:
            self.__active = True
            manager = GridManager.get_instance()
            
            if not manager:
                return []
            
            for row in range(4):
                plant_name = manager.notes_grid[row][self.column_index]
                if plant_name and plant_name.lower() in GridManager.PLANT_NOTES:
                    note = GridManager.PLANT_NOTES[plant_name.lower()]
                    octave = GridManager.ROW_OCTAVES[row]
                    return [SoundMessage(
                        player,
                        f"{note}{octave}.mp3",
                        volume=0.7,
                        repeat=False
                    )]
        return []

    def player_exited(self, player) -> List[Message]:
        self.__active = False
        return []
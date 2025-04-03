from .imports import *
from typing import TYPE_CHECKING, List
from .GridManager import GridManager

if TYPE_CHECKING:
    from Player import HumanPlayer
    from message import Message, DialogueMessage, SoundMessage
    from GridManager import GridManager
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import UtilityObject
    from tiles.map_objects import Observer

class MusicalPressurePlate(UtilityObject):
    def __init__(self):
        super().__init__("pressure_plate", passable=True)
        self.__active = False


    # not used, but does not run without this
    def update(self) -> List[Message]:
        return []

    # when player steps on pressure plate
    def player_entered(self, player) -> List[Message]:
        if not self.__active:
            self.__active = True
            messages = []
            
            from .GridManager import GridManager
            manager = GridManager._instance
            
            # checks whether grid manager is initialized
            if not manager:
                return [DialogueMessage(
                    self,
                    player,
                    "Musical garden system isn't ready yet!",
                    "error"
                )]
            
            grid_valid = all(
                len(row) == 12 for row in manager.notes_grid
            ) and len(manager.notes_grid) == 4
            
            if not grid_valid:
                return [DialogueMessage(
                    self,
                    player,
                    "Garden grid configuration is invalid!",
                    "error"
                )]
            
            # this is not working at the moment. It always says that there are no plants planted, even after the user plants some down. FIX
            has_plants = any(
                isinstance(cell, str) and cell.lower() in GridManager.PLANT_NOTES
                for row in manager.notes_grid
                for cell in row
            )
            
            # if plants are on, it plays sound, if else, it displays a message to plant
            if has_plants:
                sound_messages = manager.play_sequence(player)
                
                if sound_messages:
                    messages.extend(sound_messages)
                    messages.insert(0, DialogueMessage(
                        self,
                        player,
                        "Playing your garden melody!",
                        "music_note"
                    ))
                else: 
                    messages.append(DialogueMessage(
                        self,
                        player,
                        "The garden is silent...",
                        "exclamation"
                    ))
            else:
                messages.append(DialogueMessage(
                    self,
                    player,
                    "Plant some flowers to make music!",
                    "exclamation"
                ))
            
            return messages
        return []

    # when not on pressure plate
    def player_exited(self, player) -> List[Message]:
        self.__active = False
        return []
from .imports import *
from typing import TYPE_CHECKING,List, Dict, Optional
from .GardenGrid import GardenGrid
from .Observer import PlantObserver

if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from message import SoundMessage

class GridManage(PlantObserver):
    PLANT_NOTES = {
        "Rose": "A",
        "Tulip": "B",
        "Daisy": "C",
        "Sunflower": "D",
        "Iris": "E",
        "Lilac": "F",
        "Orchid": "G",
    }
    ROW_OCTAVES = [2, 3, 4, 5]

    def __init__(self, garden_grid):
        self.notes_grid: List[List[Optional[str]]] = [
            [None for _ in range(12)] 
            for _ in range(4)
        ]
        garden_grid.attach(self)
        self.grid = self.notes_grid

    def update_grid(self, new_grid: List[List[Optional[str]]]):
        self.notes_grid = new_grid
        self.grid = new_grid

    def on_plant_placed(self, row: int, col: int, plant_name: str) -> None:
        self.notes_grid[row][col] = plant_name
        
    def on_plant_removed(self, row: int, col: int, plant_name: str) -> None:
        self.notes_grid[row][col] = None

    def play_column(self, column: int, recipient) -> Optional[SoundMessage]:
        for row in range(4):
            plant_name = self.notes_grid[row][column]
            if plant_name and plant_name in self.PLANT_NOTES:
                note = self.PLANT_NOTES[plant_name]
                octave = self.ROW_OCTAVES[row]
                return SoundMessage(
                    recipient,
                    f"resources/sound/{note}{octave}.mp3",
                    volume=0.7,
                    repeat=False
                )
        return None

    def play_sequence(self, recipient) -> List[SoundMessage]:
        sequence = []
        for col in range(12):
            sound = self.play_column(col, recipient)
            if sound:
                sequence.append(sound)
        return sequence
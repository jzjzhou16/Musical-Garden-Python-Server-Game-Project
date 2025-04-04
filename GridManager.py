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

# implements the observer pattern
# when a plant is placed or removed, the grid manager is notified
class GridManager(PlantObserver):
    # each note within the grid is represented by a letter
    PLANT_NOTES = {
        "rose": "A",
        "tulip": "B",
        "daisy": "C",
        "sunflower": "D",
        "iris": "E",
        "lilac": "F",
        "orchid": "G",
    }
    # each row is represented by an octave
    ROW_OCTAVES = [2, 3, 4, 5]

    _instance = None
    
    @classmethod
    def get_instance(cls):
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.notes_grid = [[None]*12 for _ in range(4)]
        return cls._instance

    def __init__(self, garden_grid):
        if not hasattr(self, '_initialized'):
            if not isinstance(garden_grid, GardenGrid):
                raise ValueError("GridManager requires a GardenGrid instance")
            garden_grid.attach(self)
            print(f"GridManager initialized with garden grid at {id(garden_grid)}")
            self._initialized = True


    def update_grid(self, new_grid: List[List[Optional[str]]]):
        self.notes_grid = new_grid
        self.grid = new_grid
    
    # when plant is placed, used for observer
    def on_plant_placed(self, row: int, col: int, plant_name: str):
        self.notes_grid[row - 1 ][col - 1] = plant_name  # Ensure this matches your note mapping
        print(f"Registered {plant_name} at ({row},{col})")
    
    # when plant is removed,m used for observer
    def on_plant_removed(self, row: int, col: int, plant_name: str) -> None:
        self.notes_grid[row - 1][col - 1] = None

    # play plant notes from column (helper for play_sequence)
    def play_column(self, column: int, recipient) -> Optional[SoundMessage]:
        for row in range(4):
            plant_name = self.notes_grid[row][column]
            if plant_name and plant_name in self.PLANT_NOTES:
                note = self.PLANT_NOTES[plant_name]
                octave = self.ROW_OCTAVES[row]
                return SoundMessage(
                    recipient,
                    f"{note}{octave}.mp3",
                    volume=0.7,
                    repeat=False
                )
        return None

    # play all columns in sequence
    def play_sequence(self, recipient) -> List[Message]:
        sequence = []
        for col in range(12):
            sound = self.play_column(col, recipient)
            if sound:
                sequence.append(sound)
        return sequence
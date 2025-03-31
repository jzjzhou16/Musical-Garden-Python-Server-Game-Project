from imports import *
from typing import List, Dict, Optional
from message import SoundMessage

class GridManager:
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

    def __init__(self):
        self.grid = [[None for _ in range(12)] for _ in range(4)]

    def update_grid(self, new_grid: List[List[Optional[str]]]):
        self.grid = new_grid

    def play_column(self, column: int, recipient) -> Optional[SoundMessage]:
        for row in range(4):
            plant_name = self.grid[row][column]
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
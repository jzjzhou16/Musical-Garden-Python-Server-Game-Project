from .imports import *
from typing import Dict, List

class plantAudios:
    PLANT_NOTES: Dict[str, str] = {
        "Rose": "A",
        "Tulip": "B",
        "Daisy": "C",
        "Sunflower": "D",
        "Iris": "E",
        "Lilac": "F",
        "Orchid": "G",
    }
    
    NOTE_AUDIO_FILES: Dict[str, List[str]] = {
        'A': ["A2.mp3", "A3.mp3", "A4.mp3", "A5.mp3"],
        'B': ["B2.mp3", "B3.mp3", "B4.mp3", "B5.mp3"],
        'C': ["C2.mp3", "C3.mp3", "C4.mp3", "C5.mp3"],
        'D': ["D2.mp3", "D3.mp3", "D4.mp3", "D5.mp3"],
        'E': ["E2.mp3", "E3.mp3", "E4.mp3", "E5.mp3"],
        'F': ["F2.mp3", "F3.mp3", "F4.mp3", "F5.mp3"],
        'G': ["G2.mp3", "G3.mp3", "G4.mp3", "G5.mp3"],
    }

    @classmethod
    def get_plant_sound(cls, plant_name: str) -> str: 
        note = cls.PLANT_NOTES.get(plant_name)
        if note is None:
            raise ValueError(f"Error - No note found: {plant_name}")
        
        audio_files = cls.NOTE_AUDIO_FILES.get(note)

        if not audio_files:
            raise ValueError(f"Error - No audio file found: {note}")
        
        #return just the "2" key right now
        return audio_files[0]
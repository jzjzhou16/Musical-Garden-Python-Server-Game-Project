NOTE_AUDIO_FILES = {
    'A': ["A2.mp3", "A3.mp3", "A4.mp3", "A5.mp3"],
    'B': ["B2.mp3", "B3.mp3", "B4.mp3", "B5.mp3"],
    'C': ["C2.mp3", "C3.mp3", "C4.mp3", "C5.mp3"],
    'D': ["D2.mp3", "D3.mp3", "D4.mp3", "D5.mp3"],
    'F': ["F2.mp3", "F3.mp3", "F4.mp3", "F5.mp3"],
    'G': ["G2.mp3", "G3.mp3", "G4.mp3", "G5.mp3"],
}

PLANT_NOTES = {
    "Rose": "A",
    "Tulip": "B",
    "Daisy": "C",
    "Sunflower": "D",
    "Lilac": "F",
    "Orchid": "G",
}

def get_audio(plant_name: str) -> list[str]: 
    note = PLANT_NOTES.get(plant_name)

    if note:
        return NOTE_AUDIO_FILES.get(note, [])
    return []


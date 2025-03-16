from typing import Dict

class Plant:
    def __init__(self, name: str, sound: int, image: str, size: tuple[int, int]):
        self.name = name
        self.sound = sound
        self.image = image  
        self.size = size

    def play_sound(self):
        return self.sound

#Flyweight
class PlantFactory:
    _plants: Dict[str, Plant] = {}
    @staticmethod
    def getPlant(name: str) -> Plant | None:
        if name not in PlantFactory._plants:
            plant_info = {
                # fix these with actual data for each plant once found
                "rose": Plant("rose", 1, "rose.png", (1, 1)),
                "daisy": Plant("daisy", 2, "daisy.png", (1, 1)),
                "lily": Plant("lily", 3, "lily.png", (1, 1)),
            }
            if name in plant_info:
                PlantFactory._plants[name] = plant_info[name]
        return PlantFactory._plants.get(name)
                


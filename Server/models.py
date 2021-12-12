class PlantPot:
    id: int = None
    name: str = None
    max_water_amount: float = None
    min_ph_level: float = None
    max_ph_level: float = None

    def __init__(self, pid, name, max_water_amount, min_ph_level, max_ph_level):
        self.id = pid
        self.name = name
        self.max_water_amount = max_water_amount
        self.min_ph_level = min_ph_level
        self.max_ph_level = max_ph_level

    def to_json(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__.__str__()

    def __str__(self):
        return self.__dict__.__str__()


class Location:
    id: int = None
    name: str = None
    max_temperature: int = None

    def __init__(self, lid, name, max_temp):
        self.id = lid
        self.name = name
        self.max_temperature = max_temp

    def to_json(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__.__str__()


class Repository:
    id: int = None
    location: str = None
    plant_pot: str = None
    time: str = None
    water_level: int = None
    ph_level: str = None
    needs_water: bool = None

    def __init__(self, rid, time, water_level, ph_level, location, plant_pot, min_ph, max_ph, water_amount = None):
        self.id = rid
        self.location = location
        self.plant_pot = plant_pot
        self.time = time
        self.water_level = water_level
        if ph_level is not None:
            if ph_level < min_ph:
                self.ph_level = "POOR"
            elif ph_level > max_ph:
                self.ph_level = "EXCEED"
            else:
                self.ph_level = "GOOD"
        else:
            self.ph_level = "N/A"

        if water_amount is None:
            self.needs_water = False
        else:
            if water_level < water_amount:
                self.needs_water = True
            else:
                self.needs_water = False

    def to_json(self):
        return self.__dict__

    def __repr__(self):
        return self.__dict__.__str__()
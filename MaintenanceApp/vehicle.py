class Vehicle:
    def __init__(self, vin, year=None, make=None, model=None):
        self.vin = vin
        self.year = year
        self.make = make
        self.model = model

    def to_dict(self):
        return {
            "vin": self.vin,
            "year": self.year,
            "make": self.make,
            "model": self.model
        }
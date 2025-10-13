from base_model import BaseModel

class Amenity(BaseModel):
    existing_names = set()  # in-memory store of amenities

    def __init__(self, name):
        super().__init__()  # initialise UUID and timestamps

        self.name = str(name).strip()  # strip (remove) whitespace before/after string

        self.validate()

        Amenity.existing_names.add(self.name)  # add amenity name after validation

    def validate(self):
        if not self.name:
            raise ValueError("Amenity name is required")
        if len(self.name) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
        if self.name in Amenity.existing_names:
            raise ValueError(f"Amenity {self.name} already exists")

from .base_model import BaseModel

class Amenity(BaseModel):

    def __init__(self, name):
        super().__init__()  # initialise UUID and timestamps
        self.name = name # calls setter, validation happens automatically

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name is required and cannot be empty.")
        if len(value.strip()) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
        self._name = value.strip()

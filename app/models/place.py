from base_model import BaseModel

class Place(BaseModel):
    """ This class implements the Place logic
    """
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        self.title = str(title)
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

        if not owner: # Validate to ensure owner exists
            raise ValueError("A Place must have an owner")
        
        self.validate() # Validate attribute values
        owner.add_place(self) # Link place to user

    # Property for price
    @property
    def price(self):
        return self._price

    @property.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be greater than zero")

    # Property for latitude
    @property
    def latitude(self):
        return self._latitude

    @property.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be within the range of -90 to 90")
        self._latitude = float(value)

    # Property for longitude
    @property
    def longitude(self):
        return self._longitude

    @property.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be within the range of -180 to 180")
        self._longitude = float(value)

    # Title and Description validations
    def validate(self):
        if not self.title or len(self.title) > 100:
            raise ValueError("Title must not be empty or more than 100 characters")
        
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("Description is optional but must be a string")

    # Relationship methods - reviews and amenities
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

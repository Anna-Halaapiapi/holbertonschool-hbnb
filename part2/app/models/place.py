from .base_model import BaseModel
from .amenity import Amenity

class Place(BaseModel):
    """ This class implements the Place logic
    """
    def __init__(self, title, price, latitude, longitude, owner, description=None): # -- make description optional --
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


    # -- Property for title --
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not value or len(value.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title must not exceed 100 characters")
        self.title = value.strip()


    # Property for price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be greater than zero")
        self._price = float(value)

    # Property for latitude
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
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

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be within the range of -180 to 180")
        self._longitude = float(value)


# Title and Description validations
    def validate(self):
        # -- local import of User to prevent circular loop (importing User and Place when app is run) --
        from .user import User

        if not self.title or len(self.title) > 100:
            raise ValueError("Title must not be empty or more than 100 characters")
        
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("Description is optional but must be a string")

        if not self.owner: # -- Validate to ensure owner exists --
            raise ValueError("A Place must have an owner")

        # -- Validate owner type (User) --
        if not isinstance(self.owner, User):
            raise TypeError("Owner must be an instance of User")


    # Relationship methods - reviews and amenities
    def add_review(self, review):
        """Add a review to the place."""
        from .review import Review
        if not isinstance(review, Review):
            raise TypeError("You can only add a Review instance to a Place") # -- Validation check for Review instance (to append to) --
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if not isinstance(amenity, Amenity):
            raise TypeError("You can only add an Amenity instance to a Place") # -- Validation check for Amenity instance (to append to) --
        self.amenities.append(amenity)

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

    def validate(self):
        if not self.title or len(self.title) > 100:
            raise ValueError("Title must not be empty or more than 100 characters")
        
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("Description is optional but it must be a string")
        
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a positive value")
        
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be within -90 to 90")
        
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be within -180 to 180")
        
        # if not self.owner or not isinstance(self.owner, User): # must be a User instance creating a place
            # raise ValueError("Owner must be an instance of User")

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

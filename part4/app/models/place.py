from .base_model import BaseModel
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from app.models.amenity import association_table

class Place(BaseModel):
    """ This class implements the Place logic
    """
    __tablename__ = 'places'
    # sqlalchemy model mapping for place
    id = db.Column("id", db.String(100), primary_key=True)
    _title = db.Column("title", db.String(100), nullable=False)
    description = db.Column("description", db.String(120), nullable=True)
    _price = db.Column("price", db.Float, nullable=False)
    _latitude = db.Column("latitude", db.Float, nullable=False)
    _longitude = db.Column("longitude", db.Float, nullable=False)

    #sqlalchemy relationship mapping for place
    user_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', back_populates='places', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=association_table, back_populates='places', lazy=True,)
    
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

       
        self.validate() # Validate attribute values
        #owner.add_place(self) # Link place to user


    # -- Property for title --
    @hybrid_property
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
        self._title = value.strip()

    @title.expression
    def title(cls):
        return cls._title

    # Property for price
    @hybrid_property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be greater than zero")
        self._price = float(value)

    @price.expression
    def price(cls):
        return cls._price
    

    # Property for latitude
    @hybrid_property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be within the range of -90 to 90")
        self._latitude = float(value)

    @latitude.expression
    def latitude(cls):
        return cls._latitude
    

    # Property for longitude
    @hybrid_property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be within the range of -180 to 180")
        self._longitude = float(value)

    @longitude.expression
    def longitude(cls):
        return cls._longitude
    

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
        from .amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("You can only add an Amenity instance to a Place") # -- Validation check for Amenity instance (to append to) --
        self.amenities.append(amenity)

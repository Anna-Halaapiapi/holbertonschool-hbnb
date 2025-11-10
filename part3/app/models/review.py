from .base_model import BaseModel
from .user import User
from .place import Place
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property

class Review(BaseModel):
    """ This module represents a review for a Place - written by a User"""
    # sqlaclehmy model mapping for review
    __tablename__ = 'reviews'

    id = db.Column("id", db.String(100), primary_key=True)
    _text = db.Column("text", db.String(120), nullable=False)
    _rating = db.Column("rating", db.Integer, nullable=False)

    #sqlalchemy relationship mapping for review
    place_id = db.Column(db.String(100), db.ForeignKey('places.id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
    def __init__(self, text, rating, place, user):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        # Link review to place
        self.place.add_review(self)


    # -- Text attribute / validation -- 
    @hybrid_property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text is required.")
        self._text = value.strip()

    @text.expression
    def text(cls):
        return cls._text
    
    # -- Rating attribute / validation --
    @hybrid_property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self._rating = value

    @rating.expression
    def rating(cls):
        return cls._rating

    # -- Place attribute / validation --
    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise TypeError("A Place instance must exist.")
        self._place = value


    # -- User attribute / validation --
    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("A User instance must exist.")
        self._user = value

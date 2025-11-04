from .base_model import BaseModel
from .user import User
from .place import Place

class Review(BaseModel):
    """ This module represents a review for a Place - written by a User"""

    def __init__(self, text, rating, place, user):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        # Link review to place
        self.place.add_review(self)


    # -- Text attribute / validation -- 
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text is required.")
        self._text = value.strip()


    # -- Rating attribute / validation --
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self._rating = value


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

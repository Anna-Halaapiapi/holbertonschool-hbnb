from .base_model import BaseModel
from .user import User
from .place import Place

class Review(BaseModel):
    """ This module implements the Review logic
    """
    def __init__(self, text, rating, place, user):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        self.validate() # Validate attribute values

    def validate(self):
        if self.text is None or not isinstance(self.text, str):
            raise ValueError("content of review is required")

        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be within 1 to 5")

        if not self.place or not isinstance(self.place, Place): # must be a Place instance being reviewed
            raise ValueError("Place instance must exist")
                
        if not self.user or not isinstance(self.user, User): # must be a User instance leaving review
            raise ValueError("User instance must exist")



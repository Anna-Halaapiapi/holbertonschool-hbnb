from .base_model import BaseModel
import re  # used for matching strings based on patterns

class User(BaseModel):
    existing_emails = set()

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()  # Initialises UUID, created_at and updated_at

        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.email = str(email).lower().strip()  # remove whitespace
        self.is_admin = bool(is_admin)
        self.places = []

        self.validate()  # validates attribute values

        User.existing_emails.add(self.email)

    def validate(self):
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name is required and must be less than 50 characters")

        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name is required and must be less than 50 characters")

        if not self.email:  # checks if required email has been supplied
            raise ValueError("Email address is required")
        
        if not self.is_valid_email():  # checks if a valid email has been supplied
            raise ValueError("A valid email address is required")
        
        if self.email in User.existing_emails:  # checks if email already exists
            raise ValueError(f"Email {self.email} is already taken")

    def is_valid_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.fullmatch(pattern, self.email) is not None

    def add_place(self, place):
        """Add place to user"""
        self.places.append(place)

from .base_model import BaseModel
from app.extensions import bcrypt
import re  # used for matching strings based on patterns

class User(BaseModel):
    """
    Represents a User in the system.
    'existing_emails' is used to simulate email constraints and should be changed when implementing
    the actual database - where it is enforced by the DB layer instead.
    """

    existing_emails = set()

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()  # Initialises UUID, created_at and updated_at

        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.email = str(email).lower().strip()  # remove whitespace
        self.is_admin = bool(is_admin)
        self.places = []
        self.password = None


        if password:
            self.hash_password(password)

        # Register email (in-memory peristence)
        User.existing_emails.add(self.email)


    # -- First name --
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str):
            raise TypeError("First name must not be an empty string.")
        if len(value) > 50:
            raise ValueError("First name must be less than 50 characters.")
        self._first_name = value.strip()


    # -- Last name --
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str):
            raise TypeError("Last name must not be an empty string.")
        if len(value) > 50:
            raise ValueError("Last name must be less than 50 characters.")
        self._last_name = value.strip()


    # -- Email --
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value:
            raise ValueError("Email address is required.")
        if not isinstance(value, str):
            raise TypeError("Email must be a string.")

        email_clean = value.strip().lower()
        if not self.is_valid_email(email_clean):
            raise ValueError(f"Invalid email format: {email_clean}")

        self._email = email_clean


    # -- Validation Helper --
    def is_valid_email(self):
        """Check is provided email matches accepted pattern"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.fullmatch(pattern, self.email) is not None


    # -- Relationships--
    def add_place(self, place):
        """Associate Place with this user"""
        # -- add validation --
        if not isinstance(place, Place):
            raise TypeError("You can only add a Place instance to a user.")
        self.places.append(place)


    # -- Password Management --
    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not password or not isinstance(password, str):
            raise TypeError("Password cannot be an empty string.")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self.password:
            raise ValueError("Incorrect Password.")
        return bcrypt.check_password_hash(self.password, password)

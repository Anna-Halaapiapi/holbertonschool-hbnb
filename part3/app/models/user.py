from .base_model import BaseModel
from app.extensions import bcrypt
from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
import re  # used for matching strings based on patterns
import uuid

class User(BaseModel):
    """
    Represents a User in the system.
    'existing_emails' is used to simulate email constraints and should be changed when implementing
    the actual database - where it is enforced by the DB layer instead.
    """
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    _first_name = db.Column("first_name", db.String(50), nullable=False)
    _last_name = db.Column("last_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    password = db.Column("password", db.String(128), nullable=False)
    is_admin = db.Column("is_admin", db.Boolean, default=False)
    
    # sqlalchemy mapping relationships for user
    places = db.relationship('Place', back_populates='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

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
    @hybrid_property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str):
            raise TypeError("First name must not be an empty string.")
        if len(value) > 50:
            raise ValueError("First name must be less than 50 characters.")
        self._first_name = value.strip()
    
    @first_name.expression
    def first_name(cls):
        return cls._first_name


    # -- Last name --
    @hybrid_property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str):
            raise TypeError("Last name must not be an empty string.")
        if len(value) > 50:
            raise ValueError("Last name must be less than 50 characters.")
        self._last_name = value.strip()
    
    @last_name.expression
    def last_name(cls):
        return cls._last_name


    # -- Email --
    @hybrid_property
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
            raise ValueError("A valid email address is required")

        self._email = email_clean
    
    @email.expression
    def email(cls):
        return cls._email


    # -- Validation Helper --
    def is_valid_email(self, email):
        """Check is provided email matches accepted pattern"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.fullmatch(pattern, email) is not None


    # -- Relationships--
    def add_place(self, place):
        """Associate Place with this user"""
        from .place import Place
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

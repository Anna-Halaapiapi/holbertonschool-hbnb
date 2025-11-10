from .base_model import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from app.extensions import db

# sqlalchemy relationship association table for Place and Amenity
#association_table = db.Table('association_table',
                            #db.Column('places', db.Integer, db.ForeignKey('amenities', primary_key=True),
                                #db.Column('amenities', db.Integer, db.ForeignKey('places'), primary_key=True))
                                #)

class Amenity(BaseModel):
    # sqlalchemy model mapping for amenity
    #__tablename__ = 'amenities'
    #id = db.Column("id", db.String(100), primrary_key=True)
    #_name = db.Column("name", db.String(50), nullable=False)

    # sqlalchemy relationship mapping for amenity
    #places = db.relationship('places', secondary=association_table, lazy='subquery', back_populates='amenities')

    def __init__(self, name):
        super().__init__()  # initialise UUID and timestamps
        self.name = name # calls setter, validation happens automatically

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name is required and cannot be empty.")
        if len(value.strip()) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
        self._name = value.strip()

    @name.expression
    def text(cls):
        return cls._name

# from app.persistence.repository import InMemoryRepository
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repository import UserRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        # REPLACING INMEMREPO WITH SQLALCHEMYREPO
        # self.user_repo = InMemoryRepository()
        # self.place_repo = InMemoryRepository()
        # self.review_repo = InMemoryRepository()
        # self.amenity_repo = InMemoryRepository()

        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)


    # Placeholder method for creating a user
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, data):
        updated_user = self.user_repo.update(user_id, data)
        return updated_user

    # Placeholder method for fetching a place by ID
    def create_place(self, place_data):
        # check for owner_id in request
        owner_id = place_data.get('owner_id')
        if owner_id is None:
            raise ValueError("Owner ID is required")
        # check for exising user in repository (to link to place)
        owner = self.user_repo.get(owner_id)
        if owner is None:
            raise ValueError(f"User with ID '{owner_id}' not found")

        # validate requested amenities (by ID)
        amenity_ids = place_data.get('amenities', [])
        amenity_objects = []

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity is None:
                raise ValueError(f"Amenity with ID '{amenity_id}' not found")
            amenity_objects.append(amenity)

        # create place object
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )

        # add amenities to place object
        for amenity in amenity_objects:
            place.add_amenity(amenity)

        # store in repository
        self.place_repo.add(place)

        return place


    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place is None:
            raise ValueError(f"Place ID '{place_id}' not found")
        return place


    def get_all_places(self):
        if self.place_repo.get_all() is None:
            raise ValueError("Places not found")
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        # check if place id already exists
        valid_id = self.place_repo.get(place_id)
        if valid_id is None:
            raise ValueError(f"Place with ID '{place_id}' not found")
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    # Review methods
    def create_review(self, review_data):
        """Create a new review with validation."""
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')
        text = review_data.get('text')

        # Validate required fields
        if user_id is None or place_id is None or rating is None or not text:
            return None, "Missing required fields"

        # Validate user and place existence
        user = self.get_user(user_id)
        place = self.get_place(place_id)
        if not user:
            return None, "Invalid user_id"
        if not place:
            return None, "Invalid place_id"

        # Validate rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return None, "Rating must be an integer between 1 and 5"

        # construct review with objects
        review = Review(
            text=text,
            rating=rating,
            user=user,
            place=place
        )

        self.review_repo.add(review)
        return review, None

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)

    # Amenity methods
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name")
        amenity = Amenity(name)
        self.amenity_repo.add(amenity)
        return {"id": amenity.id, "name": amenity.name}

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        return {"id": amenity.id, "name": amenity.name}

    def get_amenity_by_name(self, name):
        amenities = self.amenity_repo.get_all()
        for amenity in amenities:
            if amenity.name.lower() == name.lower():
                return {'id': amenity.id, 'name': amenity.name}

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [{"id": a.id, "name": a.name} for a in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.name = amenity_data.get("name", amenity.name)
        return amenity

    # -- BOOTSTRAP METHOD FOR ADMIN --
    from app import create_app
    from app.models.user import User
    from app.extensions import db

    def bootstrap_admin():
        app = create_app()
        with app.app_context():
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                print("No admin found, creating one...")

                admin = User(
                        first_name='Super',
                        last_name='Admin',
                        email='admin@example.com',
                        password='adminpassword',
                        is_admin=True
                )
                db.session.add(admin)
                db.session.commit()

                print("Admin user created successfully!")
            else:
                print("Admin already exists — skipping creation.")

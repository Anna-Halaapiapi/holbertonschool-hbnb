from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    # def create_user(self, user_data):
        # Logic will be implemented in later tasks
        # pass

    # Placeholder method for fetching a place by ID
    # def get_place(self, place_id):
        # Logic will be implemented in later tasks
        # pass

    def create_amenity(self, amenity_data):
        # Create an amenity
        name = amenity_data.get("name")
        amenity = Amenity(name)
        self.amenity_repo.add(amenity)
        return {"id": amenity.id, "name": amenity.name}

  
    def get_amenity(self, amenity_id):
        # Retrieve an amenity by ID
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        return {"id": amenity.id, "name": amenity.name}

  
    def get_all_amenities(self):
        # Retrieve all amenities
        amenities = self.amenity_repo.get_all()
        return [{"id": a.id, "name": a.name}for a in amenities]

  
    def update_amenity(self, amenity_id, amenity_data):
        # Update an amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.name = amenity_data.get("name", amenity.name)
        return {"id": amenity.id, "name": amenity.name}

from app.models.place import Place
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.place_repo = InMemoryRepository()

    def create_place(self, place_data):
        # Sill to be completed by TM
        pass
    
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

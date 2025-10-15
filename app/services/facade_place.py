from app.models.place import Place
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.place_repo = InMemoryRepository()


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
            longitude=place_data['logitude'],
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

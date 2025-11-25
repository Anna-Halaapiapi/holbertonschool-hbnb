from abc import ABC, abstractmethod
from app.models.user import User
from app.models.review import Review
from app.extensions import db

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

# Review repository for sqlalchemy 
#class ReviewRepository(SQLAlchemyRepository):
    #def __init__(self):
        #super().__init__(Review)

    #def get_review_by_place(self, place_id):
        #return self.model.query.filter_by(place_id=place_id).first()

# REPLACING INMEMREPO WITH SQLALCHEMYREPO
# class InMemoryRepository(Repository):
#     def __init__(self):
#         self._storage = {}

#     def add(self, obj):
#         self._storage[obj.id] = obj

#     def get(self, obj_id):
#         return self._storage.get(obj_id)

#     def get_all(self):
#         return list(self._storage.values())

#     def update(self, obj_id, data):
#         obj = self.get(obj_id)
#         if obj:
#             obj.update(data)
#             return obj
#         return None

#     def delete(self, obj_id):
#         if obj_id in self._storage:
#             del self._storage[obj_id]
#             return True
#         return False

#     def get_by_attribute(self, attr_name, attr_value):
#         return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

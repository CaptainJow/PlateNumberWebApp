from db import db
from models.collection import CollectionModel

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    collection = db.relationship("CollectionModel", backref="user", uselist=False)

    def create_collection(self):
        collection = CollectionModel(name=f"{self.username}'s Collection")
        self.collection = collection
        db.session.add(collection)
        db.session.commit()
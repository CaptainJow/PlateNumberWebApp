import datetime
from db import db

class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(200), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"), unique = False , nullable = False)
    collection = db.relationship("CollectionModel", back_populates="items")
    created_at = db.Column(db.Date, nullable=False)
    image_name = db.Column(db.String(256), nullable=False)

    def __init__(self, value, collection_id , image_name):
        self.value = value
        self.collection_id = collection_id
        max_id = ItemModel.query.filter_by(collection_id=collection_id).order_by(ItemModel.id.desc()).first()
        self.id = max_id.id + 1 if max_id else collection_id * 1000
        self.created_at = datetime.datetime.utcnow().date()
        self.image_name = image_name
    
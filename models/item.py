from db import db

class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(20), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"), unique = False , nullable = False)
    collection = db.relationship("CollectionModel", back_populates="items")

    def __init__(self, value, collection_id):
        self.value = value
        self.collection_id = collection_id
        max_id = ItemModel.query.filter_by(collection_id=collection_id).order_by(ItemModel.id.desc()).first()
        self.id = max_id.id + 1 if max_id else collection_id * 1000
    
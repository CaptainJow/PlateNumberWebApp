from db import db

class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(20), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"), unique = False , nullable = False)
    collection = db.relationship("CollectionModel", back_populates="items")
    
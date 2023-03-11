from db import db

class CollectionModel(db.Model):
    
    __tablename__ = "collections"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship("ItemModel", back_populates="collection" ,lazy ="dynamic")


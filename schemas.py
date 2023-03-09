from marshmallow import Schema , fields

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    value = fields.Str(required=True)
    
class PlainCollectionSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class ItemSchema(PlainItemSchema):
    collection_id = fields.Int(required=True , load_only=True)
    collection = fields.Nested(PlainCollectionSchema() ,dump_only=True)

class CollectionSchema(PlainCollectionSchema):
    items = fields.Nested(ItemSchema, many=True, dump_only=True)


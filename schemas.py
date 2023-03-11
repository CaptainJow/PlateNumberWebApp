from marshmallow import Schema , fields 


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    value = fields.Str(required=True)
    created_at= fields.Str(required=True)
    
class PlainCollectionSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class ItemSchema(PlainItemSchema):
    collection = fields.Nested(PlainCollectionSchema() ,dump_only=True)

class CollectionSchema(PlainCollectionSchema):
    user_id = fields.Int(required=True, load_only=True)
    items = fields.Nested(ItemSchema, many=True, dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

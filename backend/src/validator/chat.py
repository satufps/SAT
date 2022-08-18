from marshmallow import Schema, fields
from marshmallow.validate import Length

class ChatSchema(Schema):
    message = fields.Str(required=True)
    date = fields.DateTime(required=True)
    receiver = fields.Dict(required=True)
    transmitter = fields.Dict(required=False)
    
class ReceiverSchema(Schema):
    code = fields.Str(required = True, validate=Length(min=5, max=7) )
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    
class UsersChat(Schema):
    receiver = fields.Str(required=True)
    transmitter = fields.Str(required=True)
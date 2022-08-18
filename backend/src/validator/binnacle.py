from marshmallow import fields, Schema
from marshmallow.validate import Length

class BinnacleSchema(Schema):
    text = fields.Str(required=True)
    student = fields.Str(required=True, validate=Length(equal=7))
    role = fields.Str(required=True)
    date = fields.DateTime(required=True)
    

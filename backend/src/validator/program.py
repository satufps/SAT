from marshmallow import Schema, fields
from marshmallow.validate import Length

class ProgramSchema(Schema):
    program = fields.Str(required=True)
    period = fields.Str(required=True , validate=Length(equal=6))
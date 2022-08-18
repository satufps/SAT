from marshmallow import fields, Schema
from marshmallow.validate import Length

class MeetSchema(Schema):
    role = fields.Str(required=True, validate=Length(equal=24))
    date = fields.Date(required=True)
    dateFormat = fields.Str(required=True)
    hour = fields.Str(required=False)
    ubication = fields.Str(required=True)
    student = fields.Dict(required=True)
    attendance = fields.Bool(required=True)
    state = fields.Str(required=True)
    postulation = fields.Str(required=True, allow_none=True)
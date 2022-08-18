from marshmallow import Schema, fields
from marshmallow.validate import Length, OneOf

class SuggestionSchema(Schema):
    codeStudent = fields.Str(required=True, validate=Length(equal=7))
    profit = fields.Str(required=True, validate=Length(equal=24))
    date = fields.DateTime(required=True)
    
class ResponseSuggestion(Schema):
    action = fields.Str(required=True, validate=OneOf(["accepted", "rejected"]))
    data = fields.List(fields.String(validate=Length(equal=24),required=True), required=True,)
    
class FilterSuggestion(Schema):
     filter = fields.Str(required=True, validate=OneOf(["byProfit", "byRole","byRisk","byDate","all"]))
     value = fields.Str(required=True)     
    
     
    
    
    
from marshmallow import Schema, fields, validate

class CategoryAddSchema(Schema):
    id = fields.Int(load_only=True)
    type = fields.String(
        required=True,
        validate=validate.Length(min=1, max=20),
        error_messages={"required": "Tipo é obrigatório"}
    )
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Nome é obrigatório"}
    )

    
class CategoryRequirements(Schema):
    id = fields.Int(attribute="category_id", dump_only=True)
    type = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
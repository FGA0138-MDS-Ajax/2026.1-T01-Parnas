from marshmallow import Schema, fields, validate

class PaymentAddSchema(Schema):
    id = fields.Int(load_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Nome é obrigatório"}
    )

    
class PaymentRequirements(Schema):
    id = fields.Int(attribute="payment_id", dump_only=True)
    name = fields.Str(dump_only=True)
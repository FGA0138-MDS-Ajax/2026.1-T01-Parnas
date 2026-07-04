from marshmallow import Schema, fields

class DashboardQuerySchema(Schema):
    company_id = fields.Int(
        required=True,
        error_messages={"required": "O id da empresa é obrigatório."},
    )
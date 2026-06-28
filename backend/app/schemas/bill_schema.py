from marshmallow import Schema, fields, validate

class BillSchema(Schema):
    bill_id = fields.Int(dump_only=True)

    description = fields.Str(
        required=True,
        error_messages={"required": "A descrição é obrigatória."}
    )

    amount = fields.Str(
        required=True,
        error_messages={"required": "O valor é obrigatório."}
    )

    type = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['pagar', 'receber'],
            error="O tipo deve ser exclusivamente 'pagar' ou 'receber'."
        ),
        error_messages={"required": "O tipo deve ser exclusive."}
    )

    due_date = fields.Date(
        required=True,
        error_messages={"required": "A data de vencimento (due_date) é obrigatório e deve estar no formato YYYY-MM-DD."}
    )

    category_id = fields.Int(
        required=True,
        error_messages={"required": "O ID da categoria (category_id) é obrigatório."}
    )

    status = fields.Str(dump_only=True)
    payment_date = fields.Date(dump_only=True)
    company_id = fields.Int(dump_only=True)
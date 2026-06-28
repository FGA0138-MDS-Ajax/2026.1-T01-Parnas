from marshmallow import Schema, fields, validate


class RelatorioQuerySchema(Schema):
    period = fields.String(
        required=False,
        validate=validate.OneOf(
            ["mensal", "anual"],
            error="O campo 'period' deve ser 'mensal' ou 'anual'."
        )
    )
    month = fields.Integer(
        required=False,
        error_messages={"invalid": "O campo 'month' deve ser um número inteiro."},
        validate=validate.Range(min=1, max=12, error="O campo 'month' deve estar entre 1 e 12.")
    )
    year = fields.Integer(
        required=False,
        error_messages={"invalid": "O campo 'year' deve ser um número inteiro."},
        validate=validate.Range(min=1900, max=2200, error="O campo 'year' é inválido.")
    )
    start_date = fields.Date(
        required=False,
        error_messages={"invalid": "O campo 'start_date' deve estar no formato AAAA-MM-DD."}
    )
    end_date = fields.Date(
        required=False,
        error_messages={"invalid": "O campo 'end_date' deve estar no formato AAAA-MM-DD."}
    )
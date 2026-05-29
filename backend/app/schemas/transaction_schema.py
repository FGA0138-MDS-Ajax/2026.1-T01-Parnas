from marshmallow import Schema, fields, validates, ValidationError
from datetime import date

class TransactionSchema(Schema):
    description = fields.Str(required=True, error_messages={"required": "A descrição é obrigatória."})
    amount = fields.Float(required=True, error_messages={"required": "O valor é obrigatório."})
    date = fields.Date(required=True, error_messages={"required": "A data é obrigatória."})
    type = fields.Str(required=True, error_messages={"required": "O tipo (entrada/saída) é obrigatório."})

    category_id = fields.Int(required=True, error_messages={"required":"A categoria é obrigatória."})
    company_id = fields.Int(required=True, error_messages={"required":"O ID da empresa é obrigatório"})

    @validates('amount')
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("O valor da transção deve ser estritamente positivo.")

    @validates('date')
    def validate_date(self, value):
        if value > date.today():
            raise ValidationError("A data de transação não pode ser futura.")
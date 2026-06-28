from marshmallow import Schema, fields, validate, validates, ValidationError


class SimulationCalculateDTO(Schema):
    requested_amount = fields.Float(required=True, error_messages={"required": "O valor solicitado é obrigatório."})
    deadline_month = fields.Int(required=True, error_messages={"required": "O prazo em meses é obrigatório."})
    interest_rate = fields.Float(required=True, error_messages={"required": "A taxa de juros é obrigatória."})
    modality = fields.Str(
        required=True,
        validate=validate.OneOf(['PRICE', 'SAC'], error="Modalidade deve ser 'PRICE' ou 'SAC'."),
    )

    @validates('requested_amount')
    def validate_requested_amount(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("O valor solicitado deve ser estritamente positivo.")

    @validates('deadline_month')
    def validate_deadline_month(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("O prazo deve ser de pelo menos 1 mês.")


class SimulationSaveDTO(SimulationCalculateDTO):
    pass
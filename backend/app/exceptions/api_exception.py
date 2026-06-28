class APIException(Exception):
    def __init__(self, message = "Ocorreu um erro interno ao tentar cadastrar a empresa", status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
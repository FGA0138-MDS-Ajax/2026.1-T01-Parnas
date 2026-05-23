from datetime import datetime
import re

def is_valid_password(password):
    if not password or len(password) < 8:
        return False

    has_letter = any(char.isalpha() for char in password)

    has_numbers = any(char.isdigit() for char in password)

    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>/?"

    has_special = any(char in special_chars for char in password)

    if not (has_letter and has_numbers and has_special):
        return False

    return True


def is_valid_birth_date(birth_date_str):
    if not birth_date_str:
        return False

    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = datetime.today().date()

        if birth_date > today:
            return False

        idade = today.year - birth_date.year-((today.month, today.day) < (birth_date.month, birth_date.day))

        if idade < 16:
            return False

        return True
    except ValueError:
        return False

def is_valid_cnpj(cnpj):
    cnpj_clean = re.sub(r'\D', '', cnpj)
    
    if len(cnpj_clean) != 14:
        return False, "CNPJ deve conter 14 dígitos"
    
    if cnpj_clean == cnpj_clean[0] * 14:
        return False, "CNPJ inválido"
    
    multiplicador = 5
    soma = 0
    for i in range(12):
        soma += int(cnpj_clean[i]) * multiplicador
        multiplicador += 1
        if multiplicador == 10:
            multiplicador = 2
    
    resto = soma % 11
    if(resto < 2):
        digito1 = 0
    else:
        digito1 = 11 - resto

    multiplicador = 6
    soma = 0
    for i in range(12):
        soma += int(cnpj_clean[i]) * multiplicador
        multiplicador += 1
        if multiplicador == 10:
            multiplicador = 2
    soma += digito1 * 2
    
    resto = soma % 11
    if(resto < 2):
        digito2 = 0
    else:
        digito2 = 11 - resto
    

    if int(cnpj_clean[12]) != digito1 or int(cnpj_clean[13]) != digito2:
        return False, "CNPJ inválido"
    
    return True, None
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
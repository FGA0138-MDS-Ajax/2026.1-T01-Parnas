from datetime import datetime
from app.models.user import User
from app.config import db

def register_user(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    birth_date_str = data.get('birth_date')

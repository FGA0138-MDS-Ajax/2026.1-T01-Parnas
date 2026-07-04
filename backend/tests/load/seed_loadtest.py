"""Semeia o banco de carga: usuario carga@teste.com / Senha@123 e uma empresa (id 1)."""
from datetime import date
import bcrypt

from app import create_app
from app.config import db
from app.models.user import User
from app.models.company import Company

app = create_app()
with app.app_context():
    db.create_all()

    if User.query.filter_by(email="carga@teste.com").first():
        print("usuario ja existe")
    else:
        pw = bcrypt.hashpw("Senha@123".encode(), bcrypt.gensalt()).decode()
        user = User(email="carga@teste.com", password_hash=pw, name="Carga Teste",
                    cpf="12345678901", birth_date=date(2000, 1, 1))
        db.session.add(user)
        db.session.commit()

        company = Company(name="Empresa Carga", cnpj="11.222.333/0001-81",
                          email="empresa@carga.com", phone="1130000000")
        company.users.append(user)
        db.session.add(company)
        db.session.commit()
        print("seed ok -> user", user.user_id, "company", company.company_id)

from app.config import db


class BaseRepository:
    
    def __init__(self, model):
        self.model = model
    
    def save(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity
    
    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
    
    def find_by_id(self, id):
        return db.session.get(self.model, id)
    
    def find_all(self):
        return db.session.query(self.model).all()
    
    def rollback(self):
        db.session.rollback()
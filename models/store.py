from db import db

class StoreModel(db.Model):
    """docstring for ItemModel."""

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy = 'dynamic')


    def __init__(self, name):
        self.name = name

    # JSON representation of item
    def json(self):
        return {'name': self.name, 'items': list(map(lambda x: x.json(), self.items.all()))}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

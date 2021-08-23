from .app import db


class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __repr__(self):
        return '<Pet %r>' % (self.name)

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(45))
    subject = db.Column(db.String(45))
    message = db.Column(db.String(244))

from .app import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(45))
    subject = db.Column(db.String(45))
    message = db.Column(db.String(244))

    def __repr__(self):
        return '<Client %r>' % (self.clientname)
from cvlock import login
from cvlock.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)
    folder = db.Column(db.String(40), index=True, unique=True)
    status = db.Column(db.String(8), index=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
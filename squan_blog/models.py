from . import db


class Role(db.Model):
    __tablename__ = 'rolelist'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.INTEGER)
    role_name = db.Column(db.String(32))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'userlist'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(16))
    role_id = db.Column(db.Integer, db.ForeignKey('rolelist.role_id'))

    def __repr__(self):
        return '<User %r>' % self.username

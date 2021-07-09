from Todo import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=15), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=50), nullable=False)
    todo = db.relationship('Todos', backref='owned_user', lazy=True)

    def __repr__(self):
        return f"User - {self.username} email_address - {self.email_address} - password - {self.password_hash}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        if bcrypt.check_password_hash(self.password_hash, attempted_password):
            return True


class Todos(db.Model):
    sno = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=30), unique=True, nullable=False)
    description = db.Column(db.String(length=500), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    client = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Title - {self.title} Description - {self.description}  Date - {self.date_created}"

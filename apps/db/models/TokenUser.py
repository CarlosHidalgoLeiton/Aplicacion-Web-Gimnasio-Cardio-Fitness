from apps.db.db import db


class TokenUser(db.Model):
    __tablename__ = 'tokenuser'
    IdToken = db.Column(db.Integer, primary_key=True)
    CedulaUser = db.Column(db.String(16), nullable=False)
    Token = db.Column(db.String(100), nullable=False)
    Expiration = db.Column(db.Date, nullable=False)
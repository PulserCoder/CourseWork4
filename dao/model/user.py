from enum import unique

from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre = db.Column(db.String)



class UserSchema(Schema):
    id = fields.String()
    email = fields.Email()
    password = fields.String()
    name = fields.String()
    surname = fields.String()
    favorite_genre = fields.String()


    
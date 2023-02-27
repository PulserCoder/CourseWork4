from dao.user import UserDAO
import hashlib
from flask import abort
from config import Config
import base64

class UserService():
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid), 200

    def get_all(self):
        movies = self.dao.get_all()
        return movies, 200

    def create(self, user_d):
        password = user_d.get('password')
        username = user_d.get('username')
        if 0 in [password, username]:
            abort(403)
        digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        )
        user_d['password'] = base64.b64encode(digest)
        return self.dao.create(user_d), 203

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao, 201

    def delete(self, rid):
        self.dao.delete(rid), 204

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

    def update(self, data, uid):
        user = self.get_one(uid)
        if data.get('password_1') is not None and data.get('password_2') is not None:
            if self.pass_gen(data["password_1"]) == user.password:
                user.password = self.pass_gen(data["password_2"])
            else:
                raise Exception

        if data.get('email') is not None:
            user.email = data["email"]
        if data.get('name') is not None:
            user.name = data["name"]
        if data.get('password') is not None:
            user.password = self.generate_password(data["password"])
        if data.get('surname') is not None:
            user.surname = data["surname"]
        if data.get('favorite_genre') is not None:
            user.favorite_genre = data["favorite_genre"]

        return self.dao.update(user)

    def delete(self, rid):
        self.dao.delete(rid), 204

    def pass_gen(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)
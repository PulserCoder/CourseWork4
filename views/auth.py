import base64
import calendar
import datetime
import hashlib

import jwt
from flask import request, abort
from flask_restx import Resource, Namespace
from config import Config
from dao.model.user import User

auth_ns = Namespace('auth')


@auth_ns.route('/')
class Authorization(Resource):
    def post(self):
        data = request.json
        username = data.get('username', None)
        password = data.get('password', None)
        if None in [username, password]:
            print(1)
            abort(403)
        user = User.query.filter(User.username == username).one()
        data = {
            'username': user.username,
            'role': user.role
        }
        digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        )

        if user.password == base64.b64encode(digest):
            time1 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            time2 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
            data['exp'] = calendar.timegm(time1.timetuple())
            access_token = jwt.encode(data, Config.secret, algorithm=Config.algo)
            data['exp'] = calendar.timegm(time2.timetuple())
            refresh_token = jwt.encode(data, Config.secret, algorithm=Config.algo)
            return {"access_token": access_token, "refresh_token": refresh_token}

    def put(self):
        try:
            data = jwt.decode(request.json.get('refresh_token'), Config.secret, Config.algo)
        except Exception:
            abort(403)
        data = {
            'username': data['username'],
            'role': data['role']
        }

        time1 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        time2 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(time1.timetuple())
        access_token = jwt.encode(data, Config.secret, algorithm=Config.algo)
        data['exp'] = calendar.timegm(time2.timetuple())
        refresh_token = jwt.encode(data, Config.secret, algorithm=Config.algo)
        return {"access_token": access_token, "refresh_token": refresh_token}

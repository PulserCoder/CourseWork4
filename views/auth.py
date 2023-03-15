import base64
import calendar
import datetime
import hashlib
from implemented import user_service
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
        username = data.get('email', None)
        password = data.get('password', None)
        if None in [username, password]:
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



@auth_ns.route('/register/')
class Registration(Resource):
    def post(self):
        print(1)
        data = request.json
        username = data.get('email', None)
        password = data.get('password', None)
        if None in [username, password]:
            abort(403)
        try:
            user_service.create(data)
        except Exception:
            pass
        return ""



@auth_ns.route('/login/')
class Login(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")
        if None in (email, password):
            abort(401)
        user = User.query.filter(User.email == email).one()
        try_pass = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            Config.PWD_HASH_SALT,
            Config.PWD_HASH_ITERATIONS
        )
        data = {"email": email,
                "password": password}
        if user.password == base64.b64encode(try_pass):
            time_short = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            time_long = datetime.datetime.utcnow() + datetime.timedelta(days=90)
            data['exp'] = calendar.timegm(time_short.timetuple())
            access_token = jwt.encode(data, Config.secret, algorithm=Config.algo)
            data['exp'] = calendar.timegm(time_long.timetuple())
            refresh_token = jwt.encode(data, Config.secret, algorithm=Config.algo)
            return {"access_token": access_token,
                    "refresh_token": refresh_token}
        return 403

    def put(self):
        data = request.json
        try:
            data1 = jwt.decode(data["access_token"], Config.secret, algorithms=[Config.algo])
            data2 = jwt.decode(data["refresh_token"], Config.secret, algorithms=[Config.algo])
            time_short = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            time_long = datetime.datetime.utcnow() + datetime.timedelta(days=90)
            data['exp'] = calendar.timegm(time_short.timetuple())
            access_token = jwt.encode(data1, Config.secret, algorithm=Config.algo)
            data['exp'] = calendar.timegm(time_long.timetuple())
            refresh_token = jwt.encode(data2, Config.secret, algorithm=Config.algo)
            return {"access_token": access_token,
                    "refresh_token": refresh_token}
        except:
            abort(403)



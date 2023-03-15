from flask import request
from flask_restx import Resource, Namespace

from decorators import auth_required
from implemented import user_service

us_ns = Namespace('user')
@us_ns.route('/<int:uid>')
class User(Resource):
    @auth_required
    def get(self, uid):
        return user_service.get_one(uid), 204

    @auth_required
    def patch(self, uid):
        data = request.json
        user_service.update(data, uid)
        return "", 204

@us_ns.route("/password/<int:uid>")
class UserViewPassword(Resource):
    @auth_required
    def put(self, uid):
        data = request.json
        user_service.update(data, uid)
        return "", 204
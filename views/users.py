from flask_restx import Namespace, Resource
from flask import request
from implemented import user_service
user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        return user_service.get_all()

    def post(self):
        print(3123)
        return user_service.create(request.json)


@user_ns.route('/<int:rid>')
class UserView(Resource):
    def get(self, rid):
        return user_service.get_one(rid)

    def put(self, rid):
        return user_service.update(request.json)


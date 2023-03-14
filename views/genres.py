from flask import request
from flask_restx import Resource, Namespace
from decorators import auth_required
from dao.model.genre import GenreSchema
from implemented import genre_service
from decorators import admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        rs = genre_service.get_all()
        print(rs)
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):

        return genre_service.create(request.json)


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        return genre_service.update(request.json)

    @admin_required
    def delete(self, rid):
        return genre_service.delete(rid)

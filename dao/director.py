from dao.model.director import Director, DirectorSchema


director = DirectorSchema()
directors = DirectorSchema(many=True)


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return director.dump(self.session.query(Director).get(bid))

    def get_all(self):
        return directors.dump(self.session.query(Director).all())

    def create(self, director_d):
        ent = Director(**director_d)
        self.session.add(ent)
        self.session.commit()
        return ""

    def delete(self, rid):
        director = self.get_one(rid)
        self.session.delete(director)
        self.session.commit()

    def update(self, director_d):
        director = self.get_one(director_d.get("id"))
        director.name = director_d.get("name")

        self.session.add(director)
        self.session.commit()

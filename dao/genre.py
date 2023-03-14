from dao.model.genre import Genre, GenreSchema

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return genre_schema.dump(Genre.query.get(bid))

    def get_all(self):
        return genres_schema.dump(Genre.query.all())

    def create(self, genre_d):
        ent = Genre(**genre_d)
        self.session.add(ent)
        self.session.commit()
        return ""

    def delete(self, rid):
        genre = self.get_one(rid)
        self.session.delete(genre)
        self.session.commit()

    def update(self, genre_d):
        genre = self.get_one(genre_d.get("id"))
        genre.name = genre_d.get("name")

        self.session.add(genre)
        self.session.commit()

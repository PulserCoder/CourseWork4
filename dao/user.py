from dao.model.user import User, UserSchema



user_schema = UserSchema()
class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self):
        # А еще можно сделать так, вместо всех методов get_by_*
        # t = self.session.query(Movie)
        # if "director_id" in filters:
        #     t = t.filter(Movie.director_id == filters.get("director_id"))
        # if "genre_id" in filters:
        #     t = t.filter(Movie.genre_id == filters.get("genre_id"))
        # if "year" in filters:
        #     t = t.filter(Movie.year == filters.get("year"))
        # return t.all()
        ll = []
        for el in self.session.query(User).all():
            ll.append(user_schema.dump(el))
        return ll
    def create(self, user):
        user = User(**user)
        self.session.add(user)
        self.session.commit()
        return ""

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.username = user_d.get("username")
        user.password = user_d.get("password")
        user.role = user_d.get("role")

        self.session.add(user)
        self.session.commit()

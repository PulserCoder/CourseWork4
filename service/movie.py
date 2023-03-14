from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, filters):
        if filters.get("director_id") is not None:
            movies = self.dao.get_by_director_id(filters.get("director_id"))
        elif filters.get("genre_id") is not None:
            movies = self.dao.get_by_genre_id(filters.get("genre_id"))
        elif filters.get("year") is not None:
            movies = self.dao.get_by_year(filters.get("year"))
        else:
            if filters.get("page") is not None and filters.get("status") is not None:
                movies = self.dao.get_all(page=filters.get("page"), status=filters.get("status"))
            elif filters.get("page") is not None:
                movies = self.dao.get_all(page=filters.get("page"))
            elif filters.get("status") is not None:
                movies = self.dao.get_all(status=filters.get("status"))
            else:
                movies = self.dao.get_all()
        return movies

    def create(self, movie_d):
        return self.dao.create(movie_d)

    def update(self, movie_d):
        self.dao.update(movie_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)

from repository import find_all, query
from nmf import NMF
import numpy as np


class Recommender:

    def __init__(self):
        self.data = None
        self.users = None
        self.movies = None
        self.ratings = None
        self.nmf = None
        self.user_id_index_map = None
        self.movie_id_index_map = None

    @staticmethod
    def fetch_users(threshold=0, ids=[]):
        """
        :param ids:
            Only fetch users with the given user ids.
        :param threshold:
            Fetch only users that submitted >threshold ratings.
        """
        where_expr = f"and id in ({','.join(ids)})" if len(ids) > 0 else ""
        return np.array(
            query(
                f"""
                select u.id from \"user\" as u 
                where (select count(*) from rating where userId=u.id) > {threshold}
                {where_expr}
                """)
        ).flatten()

    @staticmethod
    def fetch_movies(user_ids=np.array([])):
        """
        :param user_ids:
            Fetch only movies that were watched by at least 1 user in this array.
        """
        where_expr = f"where r.userid in ({', '.join(map(lambda x: str(x), user_ids))})" if len(user_ids) > 0 else ""
        return np.array(
            query(
                f"""
                select m.id from "movie" as m 
                where m.id in (
                    select distinct r.movieId from rating as r
                    {where_expr}
                )
                """)
        ).flatten()

    def load(self, verbose=True):
        print("Loading data from db...")
        self.users = Recommender.fetch_users(threshold=10)
        self.movies = Recommender.fetch_movies(self.users)
        self.ratings = np.array(find_all("rating", fields=['movieId', 'userId', 'rating']))
        if verbose:
            print(f"Loaded {len(self.users)} users")
            print(f"Loaded {len(self.movies)} movies")
            print(f"Loaded {len(self.ratings)} ratings")

    def build(self, verbose=True):
        ratings_map = {}
        self.user_id_index_map = {}
        self.movie_id_index_map = {}

        for row in self.ratings:
            movie_id, user_id, rating = row
            ratings_map[(movie_id, user_id)] = rating

        data = np.zeros(shape=(len(self.movies), len(self.users)))
        for i, movie_id in enumerate(self.movies):
            self.movie_id_index_map[movie_id] = i
            for j, user_id in enumerate(self.users):
                self.user_id_index_map[user_id] = j
                t = (movie_id, user_id)
                data[i, j] = 0 if t not in ratings_map else ratings_map.get(t)
        self.data = data

    def train(self):
        self.nmf = NMF(rank=10, max_iter=10)
        print("Training model...")
        self.nmf.fit(self.data, verbose=True)

    def predict_rating(self, user_id, movie_id):
        if self.nmf is None:
            raise Exception("NMF not trained")
        if user_id not in self.user_id_index_map:
            raise Exception("User not present in model")
        if movie_id not in self.movie_id_index_map:
            raise Exception("Movie not present in model")

        user_index = self.user_id_index_map[user_id]
        movie_index = self.movie_id_index_map[movie_id]
        return self.nmf.predict(movie_index, user_index)

    def top_recommendations(self, user_id, count=100):
        results = []
        for movie_id in self.movie_id_index_map:
            rating = self.predict_rating(user_id, movie_id)
            # TODO: only include unseen movies
            results.append([movie_id, rating])
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:count]

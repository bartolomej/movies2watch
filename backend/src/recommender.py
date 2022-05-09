from repository import find_all, query
from nmf import NMF
import numpy as np


class Recommender:

    def __init__(self):
        self.data = None
        self.users = None
        self.movies = None
        self.nmf = None
        self.user_index_map = None
        self.movie_index_map = None

    @staticmethod
    def fetch_users(threshold=0):
        """
        :param threshold:
            Fetch only users that submitted >threshold ratings.
        """
        return np.array(
            query(
                f"""
                select id from \"user\" as u 
                where (select count(*) from rating where userId=u.id) > {threshold}
                """)
        ).flatten()

    @staticmethod
    def fetch_movies(users=np.array([])):
        """
        :param users:
            Fetch only movies that were watched by at least 1 user in this array.
        """
        user_ids = ', '.join(map(lambda x: str(x), users))
        return np.array(
            query(
                f"""
                select m.id from "movie" as m 
                where m.id in (select distinct r.movieId from rating as r where r.userId in ({user_ids}))
                """)
        ).flatten()

    def load(self, verbose=True):
        print("Loading data from db...")
        users = Recommender.fetch_users(threshold=100)
        movies = Recommender.fetch_movies(users)
        ratings = np.array(find_all("rating", fields=['movieId', 'userId', 'rating']))

        ratings_map = {}
        self.user_index_map = {}
        self.movie_index_map = {}

        for row in ratings:
            movie_id, user_id, rating = row
            ratings_map[(movie_id, user_id)] = rating

        data = np.zeros(shape=(len(movies), len(users)))
        for i, movie_id in enumerate(movies):
            self.movie_index_map[movie_id] = i
            for j, user_id in enumerate(users):
                self.user_index_map[j] = user_id
                t = (movie_id, user_id)
                data[i, j] = 0 if t not in ratings_map else ratings_map.get(t)

        if verbose:
            print(f"Loaded {len(users)} users")
            print(f"Loaded {len(movies)} movies")

        self.data = data
        self.users = users
        self.movies = movies

    def train(self):
        self.nmf = NMF(rank=10, max_iter=10)
        print("Training model...")
        print(np.array2string(self.data))
        self.nmf.fit(self.data, verbose=True)

    def predict_rating(self, user_id, movie_id):
        if self.nmf is None:
            raise Exception("NMF not trained")
        if user_id not in self.user_index_map:
            raise Exception("User not present in model")
        if movie_id not in self.movie_index_map:
            raise Exception("Movie not present in model")

        user_index = self.user_index_map[user_id]
        movie_index = self.movie_index_map[movie_id]
        return self.nmf.predict(movie_index, user_index)

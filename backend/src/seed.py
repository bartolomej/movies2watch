from db import DB
from psycopg2.errors import UniqueViolation, ForeignKeyViolation, IntegrityConstraintViolation
import csv
from datetime import datetime
from flask import current_app
from utils import norm_text


def seed_all():
    seed_movies()
    seed_users()
    seed_ratings()
    seed_links()


def seed_movies():
    print("Seeding movies")
    conn = DB.get_connection()
    with conn.cursor() as cur:
        for row in read_seed("movies.csv"):
            if len(row) != 3:
                continue
            movie_id, title, genres = row
            try:
                cur.execute(
                    f"INSERT INTO movie (id, title, genres) VALUES ({movie_id}, '{norm_text(title)}', '{norm_text(genres)}')")
            except Exception as e:
                conn.rollback()
                raise e
    conn.commit()


def seed_users():
    print("Seeding users")
    conn = DB.get_connection()
    existing = set()
    with conn.cursor() as cur:
        for index, row in enumerate(read_seed("ratings.csv")):
            if len(row) != 4:
                continue
            user_id, movie_id, rating, timestamp = row
            if user_id in existing:
                continue
            try:
                cur.execute(f"INSERT INTO \"user\" (id) VALUES ({user_id})")
                conn.commit()
                existing.add(user_id)
            except UniqueViolation as e:
                conn.rollback()


def seed_ratings():
    print("Seeding ratings")
    conn = DB.get_connection()
    with conn.cursor() as cur:
        for index, row in enumerate(read_seed("ratings.csv")):
            if len(row) != 4:
                continue
            user_id, movie_id, rating, timestamp = row
            iso_date = datetime.fromtimestamp(int(timestamp)).isoformat()
            try:
                cur.execute(
                    f"INSERT INTO rating (rating, timestamp, movieId, userId) VALUES ({rating}, '{iso_date}', {movie_id}, {user_id})")
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)


def seed_links():
    print("Seeding links")
    conn = DB.get_connection()
    with conn.cursor() as cur:
        for index, row in enumerate(read_seed("links.csv")):
            if len(row) != 3:
                continue
            movie_id, imdb_id, tmdb_id = row
            try:
                imdb_expr = f"imdbid = {imdb_id}" if imdb_id else None
                tmdb_expr = f"tmdbid = {tmdb_id} " if tmdb_id else None
                set_expr = ','.join(list(filter(lambda x: False if x is None else True, [imdb_expr, tmdb_expr])))
                cur.execute(
                    f"UPDATE movie SET {set_expr} WHERE id = {movie_id}")
            except Exception as e:
                conn.rollback()
                raise e
            conn.commit()


def read_seed(file, row_cb=lambda x: x):
    with current_app.open_resource(f"../data/{file}") as f:
        reader = csv.reader(f.read().decode("utf8").split("\n"))
        next(reader)  # skip header row
        return reader

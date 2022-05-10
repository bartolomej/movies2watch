from db import DB
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
import csv
from datetime import datetime
from flask import current_app
from utils import norm_text


def seed_all():
    try:
        seed_movies()
    except Exception as e:
        raise e
    try:
        seed_users()
    except Exception as e:
        raise e
    try:
        seed_ratings()
    except Exception as e:
        raise e


def seed_movies():
    conn = DB.get_connection()
    with conn.cursor() as cur:
        for row in read_seed("movies.csv"):
            if len(row) != 3:
                continue
            id, title, genres = row
            try:
                cur.execute(
                    f"INSERT INTO movie (id, title, genres) VALUES ({id}, '{norm_text(title)}', '{norm_text(genres)}')")
            except Exception as e:
                conn.rollback()
                raise e
    conn.commit()


def seed_users():
    conn = DB.get_connection()
    existing = set()
    with conn.cursor() as cur:
        for index, row in enumerate(read_seed("ratings.csv")):
            if len(row) != 4:
                continue
            userId, movieId, rating, timestamp = row
            if userId in existing:
                continue
            try:
                cur.execute(f"INSERT INTO \"user\" (id) VALUES ({userId})")
                conn.commit()
                existing.add(userId)
            except UniqueViolation as e:
                conn.rollback()


def seed_ratings():
    conn = DB.get_connection()
    with conn.cursor() as cur:
        for index, row in enumerate(read_seed("ratings.csv")):
            if len(row) != 4:
                continue
            userId, movieId, rating, timestamp = row
            iso_date = datetime.fromtimestamp(int(timestamp)).isoformat()
            try:
                cur.execute(
                    f"INSERT INTO rating (id, rating, timestamp, movieId, userId) VALUES ({index}, {rating}, '{iso_date}', {userId}, {userId})")
                conn.commit()
            except ForeignKeyViolation as e:
                conn.rollback()
                pass  # ignore foreign key violation for now
            except Exception as e:
                conn.rollback()
                raise e


def read_seed(file, row_cb=lambda x: x):
    with current_app.open_resource(f"../data/{file}") as f:
        reader = csv.reader(f.read().decode("utf8").split("\n"))
        next(reader)  # skip header row
        return reader

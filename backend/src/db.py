import os
import csv
import psycopg2
from datetime import datetime
from flask import current_app
from psycopg2.errors import UniqueViolation, ForeignKeyViolation


class DB:
    conn = None

    @staticmethod
    def connect():
        try:
            DB.conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                database=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    @staticmethod
    def drop_all():
        conn = DB.get_connection()
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS rating; DROP TABLE IF EXISTS \"user\"; DROP TABLE movie;")
            conn.commit()

    @staticmethod
    def init():
        conn = DB.get_connection()
        with conn.cursor() as cur:
            with current_app.open_resource('schema.sql') as f:
                cur.execute(f.read().decode('utf8'))
                conn.commit()

    @staticmethod
    def seed():
        try:
            DB.seed_movies()
        except Exception as e:
            raise e
        try:
            DB.seed_users()
        except Exception as e:
            raise e
        try:
            DB.seed_ratings()
        except Exception as e:
            raise e

    @staticmethod
    def seed_movies():
        conn = DB.get_connection()
        with conn.cursor() as cur:
            for row in DB.read_seed("movies.csv"):
                if len(row) != 3:
                    continue
                id, title, genres = row
                try:
                    cur.execute(
                        f"INSERT INTO movie (id, title, genres) VALUES ({id}, '{DB.norm_text(title)}', '{DB.norm_text(genres)}')")
                except Exception as e:
                    conn.rollback()
                    raise e
        conn.commit()

    @staticmethod
    def seed_users():
        conn = DB.get_connection()
        existing = set()
        with conn.cursor() as cur:
            for index, row in enumerate(DB.read_seed("ratings.csv")):
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

    @staticmethod
    def seed_ratings():
        conn = DB.get_connection()
        with conn.cursor() as cur:
            for index, row in enumerate(DB.read_seed("ratings.csv")):
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

    @staticmethod
    def read_seed(file, row_cb=lambda x: x):
        with current_app.open_resource(f"../data/{file}") as f:
            reader = csv.reader(f.read().decode("utf8").split("\n"))
            next(reader)  # skip header row
            return reader

    @staticmethod
    def norm_text(value):
        return value.replace("'", "''")

    @staticmethod
    def get_connection():
        return DB.conn

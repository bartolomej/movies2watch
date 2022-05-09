import os
import psycopg2
from flask import current_app


class DB:
    conn = None

    @staticmethod
    def connect(host=None, database=None, user=None, password=None):
        def get_var(value, default):
            return value if value else default
        try:
            DB.conn = psycopg2.connect(
                host=get_var(host, os.getenv("POSTGRES_HOST")),
                database=get_var(database, os.getenv("POSTGRES_DB")),
                user=get_var(user, os.getenv("POSTGRES_USER")),
                password=get_var(password, os.getenv("POSTGRES_PASSWORD"))
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
                print("Initialising database...")
                cur.execute(f.read().decode('utf8'))
                conn.commit()
                print("Database initialised")

    @staticmethod
    def get_connection():
        return DB.conn

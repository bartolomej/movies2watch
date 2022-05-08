import os

import psycopg2


def connect():
    try:
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None


if __name__ == '__main__':
    connect()

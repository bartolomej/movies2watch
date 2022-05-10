from db import DB


def find_all(table, fields=None, limit=None):
    if fields is None:
        fields = ['*']
    limit = f"LIMIT {limit}" if limit else ""
    return query(f"SELECT {','.join(fields)} FROM \"{table}\" {limit}")


def query(sql):
    conn = DB.get_connection()
    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            conn.rollback()
            raise e


def mutation(sql):
    conn = DB.get_connection()
    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

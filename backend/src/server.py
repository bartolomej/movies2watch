import os
import re
import sched
import threading
import time
from datetime import datetime

from cerberus import Validator
from flask import request, jsonify, Flask
from flask_cors import CORS

from db import DB
from recommender import Recommender
from repository import find_all, mutation, query
from seed import seed_all
from utils import norm_text

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
r = Recommender()

s = sched.scheduler(time.time, time.sleep)
repeat_interval = 60 * 10  # update every 10min
model_needs_update = False


def update_model(sc=None):
    if not model_needs_update:
        print("Model doesn't need update")
    else:
        print("Updating model")
        # rebuild & train the entire model
        # TODO: optimise by partial update
        r.load()
        r.build()
        r.train()
    sc.enter(repeat_interval, 1, update_model, (sc,))


def model_update_handler():
    s.enter(repeat_interval, 1, update_model, (s,))
    s.run()


threading.Thread(target=model_update_handler, args=()).start()

with app.app_context():
    DB.connect()
    DB.init()
    r.load()
    r.build()
    r.train()


def get_arg(key):
    if key not in request.args:
        raise Exception(f"Arg {key} not given")
    return request.args.get(key)


def serialize_movie(movie):
    return {
        'id': movie[0],
        'title': movie[1],
        'genres': movie[2].split('|'),
        'rating': movie[3] if len(movie) > 3 else None
    }


def serialize_user(user):
    return {
        'id': user[0],
        'username': user[1]
    }


def serialize_rating(rating):
    return {
        'id': rating[0],
        'rating': rating[1],
        'timestamp': rating[2],
        'user_id': rating[3],
        'movie_id': rating[4]
    }


def validate_user(body):
    user_schema = {
        'username': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True},
    }
    v = Validator(user_schema)
    if not v.validate(body):
        raise Exception("Invalid request")


def validate_rating(body):
    rating_schema = {
        'rating': {'type': 'integer', 'required': True},
        'user_id': {'type': 'integer', 'required': True},
        'movie_id': {'type': 'integer', 'required': True},
    }
    v = Validator(rating_schema)
    if not v.validate(body):
        raise Exception("Invalid request")


@app.route('/user', methods=['POST'])
def create_user():
    body = request.json
    validate_user(body)
    existing = query(f"select * from \"user\" where username = '{body['username']}'")
    if len(existing) != 0:
        raise Exception("Username already exists")
    next_id = get_next_id("user")
    mutation(
        f"INSERT INTO \"user\" (id, username, password) VALUES ({next_id}, '{body['username']}', '{body['password']}')")
    return {
        'id': next_id,
        'message': "User created"
    }


@app.route('/user/login', methods=['POST'])
def login_user():
    body = request.json
    validate_user(body)
    rows = query(
        f"select * from \"user\" where username = '{body['username']}' and password = '{body['password']}'")
    if len(rows) == 0:
        raise Exception("User not found")
    return jsonify(serialize_user(rows[0]))


@app.route('/user/<id>')
def get_user(id):
    rows = query(f"select * from \"user\" where id = {id}")
    if len(rows) != 1:
        raise Exception("User not found")
    return jsonify(serialize_user(rows[0]))


@app.route('/movie')
def movies():
    res = None
    if 'q' in request.args:
        q = norm_text(" & ".join(re.split('[ ]+', request.args['q'])))
        res = query(f"select * from movie where to_tsvector(title) @@ to_tsquery('{q}');")
    else:
        res = find_all("movie")
    return jsonify(list(map(lambda x: serialize_movie(x), res)))


@app.route('/user')
def users():
    return jsonify(list(map(lambda x: serialize_user(x), find_all("user"))))


@app.route('/user/<id>/movie')
def user_movies(id):
    where_expr = ""
    if 'q' in request.args:
        q = norm_text(" & ".join(re.split('[ ]+', request.args['q'])))
        where_expr = f"where to_tsvector(title) @@ to_tsquery('{q}')"

    res = query(f"""
    select m.id, m.title, m.genres, r.rating from movie as m 
    left join rating as r on m.id = r.movieid and r.userid = {id} 
    {where_expr}
    order by m.id limit 100;
    """)
    return jsonify(list(map(lambda x: serialize_movie(x), res)))


@app.route('/user/<id>/recommended')
def user_recommendations(id):
    results = r.top_recommendations(int(id), count=10)
    movie_ids = list(map(lambda x: str(x[0]), results))
    movie_results = query(f"""
        select id, title, genres from movie where id in ({','.join(movie_ids)})
    """)
    return jsonify(list(map(lambda x: {
        'rating': float(x[0][1]),
        'id': int(x[1][0]),
        'title': x[1][1],
        'genres': x[1][2].split('|'),
    }, zip(results, movie_results))))


@app.route('/predict')
def recommender():
    return {
        'rating': r.predict_rating(int(get_arg("user_id")), int(get_arg("movie_id")))
    }


@app.route('/rating')
def ratings():
    return jsonify(list(map(lambda x: serialize_rating(x), find_all("rating"))))


@app.route('/rating', methods=['POST'])
def add_rating():
    global model_needs_update
    body = request.json
    validate_rating(body)
    next_id = get_next_id("rating")
    mutation(f"""
        insert into rating (id, rating, timestamp, userId, movieId)
        values ({next_id}, {body['rating']}, '{datetime.now().isoformat()}', {body['user_id']}, {body['movie_id']})
    """)
    model_needs_update = True
    return {
        'id': next_id,
        'message': "Rating added"
    }


def get_next_id(table):
    row, = query(f"select max(id) from \"{table}\"")
    return int(row[0]) + 1


@app.route('/seed')
def seed():
    seed_all()
    return "seed"


@app.route('/init')
def init():
    DB.init()
    return "Init"


@app.route('/drop')
def drop():
    DB.drop_all()
    return "dropped"


@app.errorhandler(Exception)
def handle_bad_request(e):
    return {
        'message': str(e),
        'code': 500
    }


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"),
            port=os.getenv("PORT", 8080),
            debug=os.getenv("FLASK_ENV") != 'production')

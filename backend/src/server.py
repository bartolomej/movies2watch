from flask import request, jsonify, Flask
from flask_cors import CORS
from db import DB
from seed import seed_all
from repository import find_all, mutation, query
from recommender import Recommender
from cerberus import Validator
from datetime import datetime
from utils import norm_text
import re
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
r = Recommender()

with app.app_context():
    DB.connect()
    DB.init()
    # r.load()
    # r.train()


def get_arg(key):
    if key not in request.args:
        raise Exception(f"Arg {key} not given")
    return request.args.get(key)


def serialize_movie(movie):
    return {
        'id': movie[0],
        'title': movie[1],
        'genres': movie[2].split('|')
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


@app.route('/predict')
def recommender():
    return {
        'rating': r.predict_rating(int(get_arg("user_id")), int(get_arg("movie_id")))
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


@app.route('/rating')
def ratings():
    return jsonify(list(map(lambda x: serialize_rating(x), find_all("rating"))))


@app.route('/rating', methods=['POST'])
def add_rating():
    body = request.json
    validate_rating(body)
    next_id = get_next_id("rating")
    mutation(f"""
        insert into rating (id, rating, timestamp, userId, movieId)
        values ({next_id}, {body['rating']}, '{datetime.now().isoformat()}', {body['user_id']}, {body['movie_id']})
    """)
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

from flask import request, jsonify, Flask
from flask_cors import CORS
from db import DB
from seed import seed_all
from repository import find_all, mutation, query
from recommender import Recommender
from cerberus import Validator
from datetime import datetime
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
r = Recommender()

with app.app_context():
    DB.connect()
    DB.init()
    # r.load()
    # r.train()


@app.route('/predict')
def recommender():
    def get_arg(key):
        if key not in request.args:
            raise Exception(f"Arg {key} not given")
        return int(request.args.get(key))

    return {
        'rating': r.predict_rating(get_arg("user_id"), get_arg("movie_id"))
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
    return "Success"


@app.route('/user/login', methods=['POST'])
def login_user():
    body = request.json
    validate_user(body)
    existing = query(
        f"select * from \"user\" where username = '{body['username']}' and password = '{body['password']}'")
    if len(existing) == 0:
        raise Exception("User not found")
    return jsonify(existing[0])


@app.route('/user/<id>')
def get_user(id):
    row, = query(f"select * from \"user\" where id = {id}")
    return jsonify(row)


@app.route('/movie')
def movies():
    return jsonify(find_all("movie"))


@app.route('/user')
def users():
    return jsonify(find_all("user"))


@app.route('/rating')
def ratings():
    return jsonify(find_all("rating"))


@app.route('/rating', methods=['POST'])
def add_rating():
    body = request.json
    validate_rating(body)
    next_id = get_next_id("rating")
    mutation(f"""
        insert into rating (id, rating, timestamp, userId, movieId)
        values ({next_id}, {body['rating']}, '{datetime.now().isoformat()}', {body['user_id']}, {body['movie_id']})
    """)
    return "Success"


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


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"),
            port=os.getenv("PORT", 8080),
            debug=os.getenv("FLASK_ENV") != 'production')

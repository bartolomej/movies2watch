from flask import request, jsonify, Flask
from flask_cors import CORS
from db import DB
from seed import seed_all
from repository import find_all
from recommender import Recommender
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
r = Recommender()

with app.app_context():
    DB.connect()
    DB.init()
    r.load()
    r.train()


@app.route('/predict')
def recommender():
    def get_arg(key):
        if key not in request.args:
            raise Exception(f"Arg {key} not given")
        return int(request.args.get(key))

    return {
        'rating': r.predict_rating(get_arg("user_id"), get_arg("movie_id"))
    }


@app.route('/movie')
def movies():
    return jsonify(find_all("movie"))


@app.route('/user')
def users():
    return jsonify(find_all("user"))


@app.route('/rating')
def ratings():
    return jsonify(find_all("rating"))


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

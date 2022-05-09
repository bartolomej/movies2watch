from flask import request, jsonify, Flask
from flask_cors import CORS
from db import DB
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

with app.app_context():
    DB.connect()
    DB.init()


@app.route('/movie')
def movies():
    with DB.get_connection().cursor() as cur:
        cur.execute("SELECT * FROM movie")
        return jsonify(cur.fetchall())


@app.route('/user')
def users():
    with DB.get_connection().cursor() as cur:
        cur.execute("SELECT * FROM \"user\"")
        return jsonify(cur.fetchall())


@app.route('/rating')
def ratings():
    with DB.get_connection().cursor() as cur:
        cur.execute("SELECT * FROM rating")
        return jsonify(cur.fetchall())


@app.route('/seed')
def seed():
    DB.seed()
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
    app.run(host="0.0.0.0", port=os.getenv("PORT", 8080), debug=os.getenv("FLASK_ENV") != 'production')

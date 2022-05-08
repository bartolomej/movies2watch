import sys

from flask import request, jsonify, Flask
from flask_cors import CORS
import db
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def ping_endpoint():
    conn = db.connect()
    # create a cursor
    cur = conn.cursor()
    # execute a statement
    cur.execute('SELECT version()')
    # display the PostgreSQL database server version
    return f"{cur.fetchone()}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", 8080), debug=os.getenv("FLASK_ENV") != 'production')

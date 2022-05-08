from flask import request, jsonify, Flask
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/ping')
def ping_endpoint():
    return "Pong"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", 8080), debug=os.getenv("PORT") != 'production')

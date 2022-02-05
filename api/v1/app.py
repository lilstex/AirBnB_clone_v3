#!/usr/bin/python3
from flask import Flask, jsonify
from models import storage
from os import getenv
from .views import app_views
from flask_cors import CORS

app = Flask('__name__')
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(self):
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """returns a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port)
    
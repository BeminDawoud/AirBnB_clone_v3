#!/usr/bin/python3
"""
flask app to manage the RESTful APIs
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import make_response

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(exception):
    """ closes the storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}))


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")

    app.run(host=host, port=port, threaded=True)

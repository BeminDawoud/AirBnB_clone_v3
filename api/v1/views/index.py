#!/usr/bin/python3
'''returns a JSON: "status": "OK"'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
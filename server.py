#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os
import redis
import time

# Set the value of the key: POST http://localhost:5000/<key>/<value>
# Get the value of the key: GET http://localhost:5000/<key>


app = Flask(__name__)
rdb = redis.from_url(os.environ.get("REDIS_URL"))

# set a value
@app.route('/<name>/<value>', methods=['POST'])
def set(name, value):
    rdb.set(name, value)
    return jsonify({name:value})

# fetch a value
@app.route('/<name>', methods=['GET'])
def get_name(name):
    return rdb.get(name) or ""


if __name__ == '__main__':
    app.run()
#!/usr/bin/env python3

import json
from flask import Flask, jsonify, request
import time

# Create a new key to use:  POST http://localhost:5000/new/<key>
# Set the value of the key: POST http://localhost:5000/<key>/<value>
# Get the value of the key: GET http://localhost:5000/<key>
# Clear key:                GET http://localhost:5000/clear/<key>


app = Flask(__name__)
rdb = redis.from_url(os.environ.get("REDIS_URL"))

@app.route('/clear/<name>', methods=['GET'])
def clear(name):
    rdb.set(name, "")
    return jsonify({name: ""})

# Create a new key
@app.route('/new/<name>', methods=['POST'])
def new_key(name):
    rdb.set(name, "")
    return jsonify({name: ""})

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
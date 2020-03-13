#!/usr/bin/env python3

from flask import Flask, jsonify, request
import threading
import time

# Create a new key to use:  POST http://localhost:5000/new/<key>
# Set the value of the key: POST http://localhost:5000/<key>/<value>
# Get the value of the key: GET http://localhost:5000/<key>
# Clear key:                GET http://localhost:5000/clear/<key>

app = Flask(__name__)
lock = threading.Lock()

d = {}
d['data'] = {}

def update_thread():
    global d
    while True:
        with lock:
            d['uptime'] = d.get('uptime', 0) + 1
        time.sleep(1.0)

@app.route('/clear/<name>', methods=['GET'])
def clear(name):
    global d
    with lock:
        if name in d['data']:
            del(d['data'][name])
        return jsonify({})

# Create a new key
@app.route('/new/<name>', methods=['POST'])
def new_key(name):
    with lock:
        d['data'][name] = {
                            'value': "",
                            'time': time.time()
                          }
        return jsonify(d['data'][name])

@app.route('/<name>/<value>', methods=['POST'])
def set(name, value):
    global d
    with lock:
        d['data'][name] = d['data'].get(name, {})
        # d['data'][name]['value'] = request.args.get('value') or float('nan')
        d['data'][name]['value'] = value
        d['data'][name]['time'] = time.time()
        return jsonify(d['data'][name])

@app.route('/<name>', methods=['GET'])
def get_name(name):
    with lock:
        return d['data'].get(name, {}).get('value', "")


if __name__ == '__main__':
    threading.Thread(target=update_thread).start()
    app.run(threaded=True, debug=True)
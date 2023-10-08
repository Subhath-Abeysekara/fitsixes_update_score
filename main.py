import time
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import asyncio
from cash import set_pq, get_pq_empty, get_pq
import queue
import time
# Create an empty priority queue

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})

@app.route("/")
def main():
    return "home"
@app.route("/v1/scoreupdate",methods=["POST"])
@cross_origin()
def scoreupdate():
    score = request.json['score']
    set_pq(score)
    return "success"

@app.route("/v1/getscore")
@cross_origin()
def scoreget():
    if get_pq_empty():
        return {
            "state":False
        }
    return {
        "state": True,
        "score":get_pq()
    }

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost',port=5000)

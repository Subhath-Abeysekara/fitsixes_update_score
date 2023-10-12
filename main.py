import time
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import asyncio
from cash import set_pq, get_pq_empty, get_pq
import queue
import time

from score_update import update_match_score

# Create an empty priority queue

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})

@app.route("/")
def main():
    return "home"
@app.route("/v1/scoreupdate",methods=["POST"])
@cross_origin()
def scoreupdate():
    try:
        score = request.json['score']
        return update_match_score(score['match_id'], score['key'])
    except Exception:
        return {
            "state":False,
            "error":Exception
        }

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

import time
import json

import requests
from apscheduler.triggers.interval import IntervalTrigger
from bson import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio

import env
from cash import set_pq, get_pq_empty, get_pq, remove_match
import queue
import time

from recap_score import recap_match_score
from score_update import update_match_score
from connection import connect_mongo_sensitive
collection_name = connect_mongo_sensitive()
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

@app.route("/v1/recap/<id>")
@cross_origin()
def recapscore(id):
    return recap_match_score(id)

@app.route("/v1/remove/<id>")
@cross_origin()
def clear_moves(id):
    return remove_match(id)

scheduler = BackgroundScheduler()
scheduler.start()
app.apscheduler = scheduler

def scheduled_task():
    if get_pq_empty():
        print("empty")
        return
    data = collection_name.find_one({'_id': ObjectId(env.CONNECTION_ID)})
    body = {
        "connections":data['connections'],
        "data":{
            "score":get_pq()
        }
    }
    url = "https://pue5ufow3l.execute-api.ap-south-1.amazonaws.com/dev/v1/broadcast_score"
    x = requests.post(url=url, json=body)
    print("This task runs every minute.")

# Schedule the task to run every minute
app.apscheduler.add_job(
    scheduled_task,
    trigger=IntervalTrigger(seconds=5),
    id='scheduled_task',
    name='Scheduled Task'
)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost',port=5000)

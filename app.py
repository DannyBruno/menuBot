import os
import redis
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)

db = redis.from_url(os.environ.get("REDIS_URL"))


#frontend
@app.route('/')
def hello_world():
    return 'Hello, World!'

#verify
@app.route('/webhook', methods=['GET'])
def verify():
	if request.args["hub.mode"] == "subscribe": #will later need to learn how to hide important things like this
		if not request.args["hub.verify_token"] == 'verifyMe':
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200


#message logic
@app.route('/webhook', methods=['POST'])
def webhook():
	



if __name__ == '__main__':
	app.run()

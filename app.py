import os
import redis
import sys
import json

import requests
from flask import Flask, request
#APScheduler

app = Flask(__name__)

db = redis.from_url(os.environ.get("REDIS_URL"))

'''
headers = {
	"Content-Type": "application/json"
}
'''

#initialize get started button and greeting text
greetingsPayload = {
  "setting_type":"greeting",
  "greeting":{
    "text":"University of Michigan Dining hall menus straight to your phone, every morning."
  }
}
try:
	greetingResponse = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6", data = json.dumps(greetingsPayload))
	if (greetingResponse.json() != requests.codes.ok):
		raise ConnectionError("greeting set failed")
except ConnectionError as err:
	print(err.args) 


getStartedPayload = { 
  "get_started":{
    "payload":"GET_STARTED_PAYLOAD"
  }
}
try:
	getStartedResponse = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6", data = json.dumps(getStartedPayload)) 
	if (getStartedResponse.status_code != requests.codes.ok):
		raise ConnectionError("get started set failed")
except ConnectionError as err:
	print(err.args) 





#frontend
@app.route('/')
def hello_world():
    return 'Hello, World!'




#verify
@app.route('/webhook', methods=['GET'])
def verify():
	if request.args["hub.mode"] == "subscribe": #will later need to learn how to hide important things like this
		if not request.args["hub.verify_token"] == 'verifyMe':
			return "Verification token incorrect", 403
		return request.args["hub.challenge"], 200





#message logic
@app.route('/webhook', methods=['POST'])
def webhook():

	messageObject = request.get_json()
	log(messageObject)

	#message parse logic



#periodic message send, uses database APScheduler



#at a time of day cache the menus, APScheduler




#logs messages
def log(message):
	print str(message)
	sys.stdout.flush()


if __name__ == '__main__':
	app.run()

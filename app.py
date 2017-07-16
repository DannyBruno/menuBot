import os
import redis
import sys
import json

import requests
from flask import Flask, request
#APScheduler

app = Flask(__name__)

pageAccessToken = 'EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6'


#url = os.environ.get("REDIS_URL")
#print(url)
db = redis.from_url('redis://h:p3116b29cf75492a50fe130ffeb19d111fe87d4b0daea9440e235fec5a5f14300@ec2-34-224-49-43.compute-1.amazonaws.com:45779')
db.set_response_callback('GET',int)



headers = {
	"Content-Type": "application/json"
}

#for testing###################################################
db.flushdb()

deleteMessagePayload = {
  "fields":[
    "greeting"
  ]
}
try:
	deleteMessageResponse = requests.delete("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6", data=json.dumps(deleteMessagePayload), headers=headers)
	if (deleteMessageResponse.status_code != requests.codes.ok):
		raise ConnectionError("Greeting delete failed!")
	else:
		print("Greeting deleted successfully!")
except ConnectionError as err:
	print(err) 

getGreeting = requests.get("https://graph.facebook.com/v2.6/me/messenger_profile?fields=greeting&access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6")
print (getGreeting.json(), end="\n\n")


deletegetStartedPayload = {
  "fields":[
    "get_started"
  ]
}
try:
	deletegetStartedResponse = requests.delete("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6", data=json.dumps(deletegetStartedPayload), headers=headers)
	if (deletegetStartedResponse.status_code != requests.codes.ok):
		raise ConnectionError("Get started delete failed!")
	else:
		print("Get started deleted successfully!")
except ConnectionError as err:
	print(err) 

getStarted = requests.get("https://graph.facebook.com/v2.6/me/messenger_profile?fields=get_started&access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6")
print (getStarted.json(), end="\n\n\n")



#######################################################################




#initialize get started button and greeting text
greetingsPayload = {
  "greeting":[
    {
      "locale":"default",
      "text":"Hello!"
    }
  ] 
} 
print(json.dumps(greetingsPayload))
try:
	greetingResponse = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6", data=json.dumps(greetingsPayload), headers=headers)
	#print (greetingResponse.status_code)
	print(greetingResponse.json())
	if (greetingResponse.status_code != requests.codes.ok):
		raise ConnectionError("Greeting set failed!")
	else:
		print("Greeting set successfully!")
except ConnectionError as err:
	print(err) 



getGreeting = requests.get("https://graph.facebook.com/v2.6/me/messenger_profile?fields=greeting&access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6")
print (getGreeting.json(), end="\n\n")



getStartedPayload = { 
  "get_started":{
    "payload":"GET_STARTED_PAYLOAD"
  }
}
print(json.dumps(getStartedPayload))
try:
	getStartedResponse = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6", data=json.dumps(getStartedPayload), headers=headers) 
	#print (getStartedResponse.status_code)
	print(getStartedResponse.json())
	if (getStartedResponse.status_code != requests.codes.ok):
		raise ConnectionError("get started set failed")
	else:
		print("GetStarted set successfully!")
except ConnectionError as err:
	print(err) 


getStarted = requests.get("https://graph.facebook.com/v2.6/me/messenger_profile?fields=get_started&access_token=" + pageAccessToken)
print (getStarted.json())





#frontend
@app.route('/')
def hello_world():
    return 'Hello, World!'

def sendMessage(senderID, message):
	payload = {
  		"recipient":{
  			"id":senderID
  		},
  		"message":{
  			"text": message
  		}
	}
	requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + pageAccessToken, headers=headers, data=json.dumps(payload))



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
	#print(request)
	messageObject = json.loads(request.data)
	senderID = messageObject['entry'][0]['messaging'][0]['sender']['id']
	body = messageObject['entry'][0]['messaging'][0]

	userInfo = request.get("https://graph.facebook.com/v2.6/<" + senderID + ">?fields=first_name,last_name,timezone&access_token=" + pageAccessToken)

	print(messageObject)
	if 'postback' in body:	#get started was triggered
		#print("HELLO!")
		sendMessage(senderID,"Hi " + userInfo["first_name"] + "! Welcome to menuBot! Would you like to subscribe to the service? \n(YES, NO)")
		db.set(senderID, 0)
	else:
		value = db.get(senderID)
		if value == 0 and (body['message']['text'].lower() == 'yes' or body['message']['text'].lower() == 'y'):
			db.set(senderID, 10)
			sendMessage(senderID, "Awesome! You're good to go!")
		elif value == 0 and body['message']['text'].lower() != 'yes':
			senderID(senderID, "No worries! Message back at anytime to be reprompted!")
		else:
			sendMessage(senderID, "Sorry! I'm not sure what you mean!")


#periodic message send, uses database APScheduler



#at a time of day cache the menus, APScheduler


	return "ok", 200




if __name__ == '__main__':
	app.run()

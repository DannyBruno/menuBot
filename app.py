import os
import redis
import sys
import json
from datetime import datetime
import pytz
import time
import re
import requests

from flask import Flask, request


app = Flask(__name__)
#app.config.from_object(os.environ.get('APP_SETTINGS', 'config.ProductionConfig'))

pageAccessToken = os.environ['PAGE_ACCESS_TOKEN']


#url = os.environ.get("REDIS_URL")
#print(url)
db = redis.from_url(os.environ['REDIS_URL'])
db.set_response_callback('GET',int)



headers = {
	"Content-Type": "application/json"
}

#for testing###################################################
db.flushdb()
'''
deleteMessagePayload = {
  "fields":[
    "greeting"
  ]
}
try:
	deleteMessageResponse = requests.delete("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + pageAccessToken, data=json.dumps(deleteMessagePayload), headers=headers)
	if (deleteMessageResponse.status_code != requests.codes.ok):
		raise ConnectionError("Greeting delete failed!")
	else:
		print("Greeting deleted successfully!")
except ConnectionError as err:
	print(err) 

getGreeting = requests.get("https://graph.facebook.com/v2.6/me/messenger_profile?fields=greeting&access_token=" + pageAccessToken)
print (getGreeting.json(), end="\n\n")


deletegetStartedPayload = {
  "fields":[
    "get_started"
  ]
}
try:
	deletegetStartedResponse = requests.delete("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + pageAccessToken, data=json.dumps(deletegetStartedPayload), headers=headers)
	if (deletegetStartedResponse.status_code != requests.codes.ok):
		raise ConnectionError("Get started delete failed!")
	else:
		print("Get started deleted successfully!")
except ConnectionError as err:
	print(err) 

getStarted = requests.get("https://graph.facebook.com/v2.6/me/messenger_profile?fields=get_started&access_token=" + pageAccessToken)
print (getStarted.json(), end="\n\n\n")



#######################################################################




#initialize get started button and greeting text
greetingsPayload = {
  "greeting":[
    {
      "locale":"default",
      "text":"Welcome to UmichEats!"
    }
  ] 
} 
print(json.dumps(greetingsPayload))
try:
	greetingResponse = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + pageAccessToken, data=json.dumps(greetingsPayload), headers=headers)
	#print (greetingResponse.status_code)
	print(greetingResponse.json())
	if (greetingResponse.status_code != requests.codes.ok):
		raise ConnectionError("Greeting set failed!")
	else:
		print("Greeting set successfully!")
except ConnectionError as err:
	print(err) 



getGreeting = requests.get("https://graph.facebook.com/v2.6/me/messenger_profile?fields=greeting&access_token=" + pageAccessToken)
print (getGreeting.json(), end="\n\n")



getStartedPayload = { 
  "get_started":{
    "payload":"GET_STARTED_PAYLOAD"
  }
}
print(json.dumps(getStartedPayload))
try:
	getStartedResponse = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + pageAccessToken, data=json.dumps(getStartedPayload), headers=headers) 
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


'''


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


def attemptToParse(inputString):
	inputString = inputString.replace(" ", "")
	choiceList = inputString.split(",")
	for value in choiceList:
		if not len(value) == 1:
			print("Each length was not one")
			return (False, choiceList)
		elif not value.isdigit():
			print("each value is not a digit")
			return (False, choiceList)
		elif not (int(value) > 0 and int(value) < 8):
			print("not greater than 0 and not less than 8")
			return (False, choiceList)
	choiceList = set(choiceList)
	return (True, choiceList)

def buildValue(inputList):
	index = 1
	total = 0
	for value in inputList:
		total += index*int(value)
		index *= 10
	return total

def decipherChoice(value):
	myList = []
	while (value > 0):
		next = value%10
		#print(next)
		myList.append(value%10)
		value = value//10
		#print(value)
	return myList


diningHallList = ["Bursley", "East Quad", "Markley", "Mosher-Jordan (Mojo)", "North Quad", "South Quad", "Twigs (Oxford)"]

#message logic
@app.route('/webhook', methods=['POST'])
def webhook():
	#print(request)
	messageObject = json.loads(request.data)
	senderID = messageObject['entry'][0]['messaging'][0]['sender']['id']
	print(senderID)
	body = messageObject['entry'][0]['messaging'][0]

	userInfo = requests.get("https://graph.facebook.com/v2.6/" + senderID + "?fields=first_name,last_name&access_token=" + pageAccessToken)
	userInfo = userInfo.json()
	print(userInfo)
	print(messageObject)
	if 'postback' in body:	#get started was triggered
		#print("HELLO!")
		sendMessage(senderID,"Hi " + userInfo["first_name"] + "! Welcome to menuBot! Would you like to subscribe to the service? \n(Yes, No)")
		db.set(senderID, 0)
	else:
		if db.exists(senderID):
			value = db.get(senderID)
			print("The value is %s" % value)
			if value == 0 and (body['message']['text'].lower() == 'yes' or body['message']['text'].lower() == 'y'):
				sendMessage(senderID, "Awesome! You're almost done- just select which dining halls you'd like to subscibe to:")
				sendMessage(senderID, "1. Bursley, 2. East Quad, 3. Markley, 4. Mosher-Jordan (Mojo), 5. North Quad, 6. South Quad, 7. Twigs (Oxford)")
				sendMessage(senderID, "Submit your response in format <Dining hall choice 1>, <Dining hall choice 2>, <Dining hall choice 3>")
				sendMessage(senderID, "So, for example- to select South Quad, Mojo, and East Quad respond with \"6, 4, 2\" (in any order)")
				db.set(senderID,-1)
			elif value == 0 and body['message']['text'].lower() != 'yes':
				senderID(senderID, "No worries! Message back at anytime to be reprompted!")
			elif value == -1:
				attempt = attemptToParse(body['message']['text'])
				if (attempt[0]):
					choice = buildValue(attempt[1])
					db.set(senderID, choice) #send confirmation message
					decipheredChoice = decipherChoice(choice)

					print("Choices were: %s" % decipheredChoice)

					choiceString = "You have been subscribed to "
					for key in range(0,len(decipheredChoice)-1):
						choiceString  = choiceString + diningHallList[decipheredChoice[key]-1] + ", "

					if len(decipheredChoice) != 1:
						choiceString = choiceString + "and " + diningHallList[decipheredChoice[len(decipheredChoice)-1]-1] + "."
					else:
						choiceString = choiceString + diningHallList[decipheredChoice[len(decipheredChoice)-1]-1] + "."

					sendMessage(senderID, choiceString)
					sendMessage(senderID, "If you would like to edit your selection simply message \"edit\" any time. Additionally, to unsubscribe message \"unsubscribe\" (but we'll be sad to see you go!).")
				else:
					sendMessage(senderID, "Sorry! I'm not sure what you mean. Make sure you input your selection correctly.")
					sendMessage(senderID, "Remember, to select South Quad, Mojo, and East Quad respond with \"6, 4, 2\" (in any order but seperated by commas)")
			elif value != 0:
				#if not "unsuscribe" or "edit" print informational message, otherwise unsub or allow them to alter stored value in db
				if body['message']['text'].lower() == 'unsubscribe':
					sendMessage(senderID, "You've been unsubscribed! Message back at any time to be repromted!")
					db.delete(senderID)
				elif body['message']['text'].lower() == 'edit':
					sendMessage(senderID,"You're previous selection is ready to be overwritten! Make your selection: ")
					sendMessage(senderID, "1. Bursley, 2. East Quad, 3. Markley, 4. Mosher-Jordan (Mojo), 5. North Quad, 6. South Quad, 7. Twigs (Oxford)")
					sendMessage(senderID, "Submit your response in format <Dining hall choice 1>, <Dining hall choice 2>, <Dining hall choice 3>")
					sendMessage(senderID, "So, for example- to select South Quad, Mojo, and East Quad respond with \"6, 4, 2\" (in any order)")
					db.set(senderID,-1)
				else:
					sendMessage(senderID, "I'm not sure what you mean! Type \"unsubscribe\" at any time to unsubscribe from the service or \"edit\" if you'd like to edit your selection of dining halls. (Visit menuBot.com for more advanced usage documentation)")
		else:
			##people trying to resub
			sendMessage(senderID,"Hi " + userInfo["first_name"] + "! Welcome back to menuBot! Would you like to subscribe to the service? \n(Yes, No)")
			db.set(senderID, 0)


	return "ok", 200




#TODO: frontend
@app.route('/')
def hello_world():
    return 'Hello, World!'




if __name__ == '__main__':
	app.run(port=6000, use_reloader=False)

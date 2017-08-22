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
from apscheduler.schedulers.background import BackgroundScheduler
#from config import *
#APScheduler

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
      "text":"Hello!"
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

###
'''
db.set("Dan", ["1","2","3"]);
print(db.hget("Dan"));
'''
###



scheduler = BackgroundScheduler()
diningHallList = ["Bursley", "East Quad", "Markley", "Mosher-Jordan (Mojo)", "North Quad", "South Quad", "Twigs (Oxford)"]
#datetime.datetime.now().time()

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

#for 1, 3, 4, 5, 6
#east quad just needs the %20, mosher%20jordan, north%20quad, south%20quad, location=twigs%20at%20oxford%20&output=json&date=today
diningHallList = ["Bursley", "East Quad", "Markley", "Mosher-Jordan (Mojo)", "North Quad", "South Quad", "Twigs (Oxford)"]
#strftime("%Y-%m-%d %H:%M:%S", gmtime())

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




###########_________CACHING__________############


def cacheDiningHall(responseContent, index , diningHallMenuDict):
	print("Caching!!")

	mealString = ""
	for meal in range(0,3):
		mealString = ""
		#print(responseContent['menu']['meal'][meal]['name'])						 // breakfast//lunch//dinner
		mealString = mealString + responseContent['menu']['meal'][meal]['name'] + "\n"
		print(responseContent['menu']['meal'][meal]['name'] + "\n")
		print(len(diningHallMenuDict[index]))
		BLDindex = len(diningHallMenuDict[index])
		traitSet = set()
		if (type(responseContent['menu']['meal'][meal]['course']) == type({})):
			if (type(responseContent['menu']['meal'][meal]['course']['menuitem']) == type({})):	#not serving anything
				mealString = mealString + responseContent['menu']['meal'][meal]['course']['menuitem']['name']
			else:
				for item in range(0,len(responseContent['menu']['meal'][meal]['course']['menuitem'])):
					mealString = mealString + responseContent['menu']['meal'][meal]['course']['menuitem'][item]['name']
			#print("Start of this1..")
			#print(mealString)
			mealString = mealString.rstrip("\n")
			diningHallMenuDict[index].append(mealString + "\n")
			mealString = ""
			#print("End of this1..")
		else:
			for course in range(0,len(responseContent['menu']['meal'][meal]['course'])):
				#print(responseContent['menu']['meal'][meal]['course'][course]['name'])		#signature baked goods etc
				mealString = mealString + "-" + responseContent['menu']['meal'][meal]['course'][course]['name'] + "-\n"
				if (type(responseContent['menu']['meal'][meal]['course'][course]['menuitem']) != type({})):		#menu item names
					for menuitem in range(0,len(responseContent['menu']['meal'][meal]['course'][course]['menuitem'])):
						#print(responseContent['menu']['meal'][meal]['course'][course]['menuitem'][menuitem]['name'])
						mealString = mealString + responseContent['menu']['meal'][meal]['course'][course]['menuitem'][menuitem]['name']
						if ('trait' in responseContent['menu']['meal'][meal]['course'][course]['menuitem'][menuitem]):	#menu item traits
							mealString = mealString.rstrip()
							mealString = mealString + " - ("
							for trait in responseContent['menu']['meal'][meal]['course'][course]['menuitem'][menuitem]['trait']:
								if (responseContent['menu']['meal'][meal]['course'][course]['menuitem'][menuitem]['trait'][trait] == 'glutenfree'):
									mealString = mealString + 'gluten free, '
									traitSet.add("gluten free")
								else:
									mealString = mealString + responseContent['menu']['meal'][meal]['course'][course]['menuitem'][menuitem]['trait'][trait] + ", "
									traitSet.add(responseContent['menu']['meal'][meal]['course'][course]['menuitem'][menuitem]['trait'][trait])
							mealString = mealString.rstrip(", ")
							mealString = mealString + ")"
						mealString = mealString + "\n"
				else:
					#print(responseContent['menu']['meal'][meal]['course'][course]['menuitem']['name'])		#menu item names
					mealString = mealString + responseContent['menu']['meal'][meal]['course'][course]['menuitem']['name']
					if ('trait' in responseContent['menu']['meal'][meal]['course'][course]['menuitem']):

						mealString = mealString.rstrip()
						mealString = mealString + " - ("
						for trait in responseContent['menu']['meal'][meal]['course'][course]['menuitem']['trait']:
							trait
							if (responseContent['menu']['meal'][meal]['course'][course]['menuitem']['trait'] == 'glutenfree'):
								mealString = mealString + 'gluten free, '
								traitSet.add("gluten free")
							else:	
								mealString = mealString + responseContent['menu']['meal'][meal]['course'][course]['menuitem']['trait'][trait] + ", "
								traitSet.add(responseContent['menu']['meal'][meal]['course'][course]['menuitem']['trait'][trait])
						mealString = mealString.rstrip(", ")
						mealString = mealString + ")"
					mealString = mealString + "\n"
				mealString = mealString + "\n"
				#print("Start of this3..")
				#print(mealString)
				mealString = mealString.rstrip("\n")
				diningHallMenuDict[index].append(mealString + "\n")
				mealString = ""
				#print("End of this3..")
		#mealString = mealString
		#print(mealString.rstrip("\n"))				#send breakfast lunch and dinner here
		#print("I am being added.."
		print("BLD index, should be breakfast lunch or dinner: %s" % diningHallMenuDict[index][BLDindex])
		#print(traitSet)
		if (len(traitSet) != 0):
			traitSetString = ""
			traitSet = list(traitSet)
			for trait in range(0,len(traitSet)):
				traitSetString = traitSetString + traitSet[trait] + ", "
			traitSetString = traitSetString.rstrip(", ")
			#print(traitSetString)

			#split with returns
			splitStr = diningHallMenuDict[index][BLDindex].split("\n", 1)
			print(splitStr)
			splitStr[0] = splitStr[0] + "\n! " + traitSetString + " !" + "\n\n"

			putBacktogether = ""
			for string in range(0, len(splitStr)):
				putBacktogether = putBacktogether + splitStr[string]

			diningHallMenuDict[index][BLDindex] = putBacktogether
		print("BLD index, should have traits added: %s" % diningHallMenuDict[index][BLDindex])
	#("BLD index, should be breakfast lunch or dinner: %s" % diningHallMenuDict[index][BLDindex])
	print("DONE CACHING..")
#.rstrip("\n")
def pullMenus(diningHallMenuDict, diningHallList):
	for entry in range(0,7):
		print("--" + diningHallList[entry] + "--") #send with just name here
		print("I am being added..")
		diningHallMenuDict[entry] = []
		diningHallMenuDict[entry].append("--" + diningHallList[entry] + "--")
		requestURL = 'http://www.housing.umich.edu/files/helper_files/js/xml2print.php?location='
		if (entry == 3):
			requestURL = requestURL + "mosher%20jordan" + '%20DINING%20HALL&output=json&date=today'
			#print(requestURL)
		elif (entry == 6):
			print("caching oxford")
			requestURL = requestURL + 'twigs%20at%20oxford%20&output=json&date=today'
			#print(requestURL)
		else:
			requestURL = requestURL + diningHallList[entry].replace(" ", "%20") + '%20DINING%20HALL&output=json&date=today'
		cacheDiningHall(json.loads(requests.get(requestURL).content), entry, diningHallMenuDict)
	for entry in diningHallMenuDict:				#sanity check
		for i in range(0, len(diningHallMenuDict[entry])):
			print("new message..")
			print(diningHallMenuDict[entry][i])
			print("end of message..")


diningHallList = ["Bursley", "East Quad", "Markley", "Mosher-Jordan (Mojo)", "North Quad", "South Quad", "Twigs (Oxford)"]

diningHallMenuDict = {}

print("Time..")
tz = pytz.timezone('US/Eastern')
easternNow = datetime.now(tz)
print(easternNow)
print("Time..")

#populates with info
scheduler.add_job(pullMenus, 'cron', [diningHallMenuDict, diningHallList], hour=3, minute=33, second=10, timezone=pytz.timezone('US/Eastern'))


#mylist = [1,2,3]

#pullMenus(diningHallMenuDict, diningHallList)
#print(diningHallMenuDict[0])


#pullMenus(diningHallMenuDict, diningHallList)
###########################__________________________###########################
def sendToSubscribers():
	print("Sending to subscribers!!")
	#print("The keys in keys: %s" % db.keys())

	for key in db.keys():
		#print("size of keys %s" % len(db.keys()))
		if db.get(key.decode('utf-8')) > 0:
			print("key %s: %s" % (n, key.decode('utf-8')))
			choiceList = decipherChoice(db.get(key.decode('utf-8')))
			print(choiceList)
			userInfo = requests.get("https://graph.facebook.com/v2.6/" + key.decode('utf-8') + "?fields=first_name,last_name&access_token=" + pageAccessToken).json()
			sendMessage(key.decode('utf-8'), "----------------------")
			sendMessage(key.decode('utf-8'), "Good Morning " + userInfo["first_name"] + "!")
			sendMessage(key.decode('utf-8'), "It's " + time.strftime("%a, %d %b %Y") + ".")
			for choice in range(0,len(choiceList)):
				messageperHall = ""
				messageList = []
				for i in range(0, len(diningHallMenuDict[choiceList[choice]])):


					if (diningHallMenuDict[choiceList[choice]][i][:5] == "LUNCH" or diningHallMenuDict[choiceList[choice]][i][:6] == "DINNER" or diningHallMenuDict[choiceList[choice]][i][:9] == "BREAKFAST"):
						#submit current str and start new one with this starting
						messageList.append(messageperHall)
						messageperHall = diningHallMenuDict[choiceList[choice]][i]
					else:
						messageperHall = messageperHall + diningHallMenuDict[choiceList[choice]][i] + "\n"
						if (len(messageperHall) > 250):
							messageList.append(messageperHall)
							messageperHall = ""
			
				messageList.append(messageperHall)
				print(messageList)
				for index in range(0, len(messageList)):
					print("Block..")
					print(len(messageList[index]))
					print("Block..")
					sendMessage(key.decode('utf-8'), messageList[index])

		sendMessage(key.decode('utf-8'), "If you would like to edit your selection simply message \"edit\" any time. Additionally, to unsubscribe message \"unsubscribe\" (but we'll be sad to see you go!).")
		sendMessage(key.decode('utf-8'), "----------------------")




scheduler.add_job(sendToSubscribers, 'cron', hour=3, minute=33, second=45, timezone=pytz.timezone('US/Eastern'))


#print(diningHallMenuDict)
scheduler.start()

'''______GOOD TESTING, NEED TO MAKE SURE LUNCH STARTS A NEW MSG ETC, MAY USE SPECIAL CHAR______'''
#db.set('1458256307549428', 3456)

#pullMenus(diningHallMenuDict, diningHallList)

#time.sleep(5)

#sendToSubscribers()



if __name__ == '__main__':
	app.run(port="6000", use_reloader=False)

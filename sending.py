import redis
import requests
import json
import time
from datetime import datetime
import os

db = redis.from_url(os.environ['REDIS_URL'], db= 0)
#db = redis.from_url('redis://h:p3116b29cf75492a50fe130ffeb19d111fe87d4b0daea9440e235fec5a5f14300@ec2-34-224-49-43.compute-1.amazonaws.com:45779', db= 0)
db.set_response_callback('GET',int)
pageAccessToken = os.environ['PAGE_ACCESS_TOKEN']
#pageAccessToken = 'EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6'

def sendMessage(senderID, message):
	headers = {
	"Content-Type": "application/json"
	}
	payload = {
  		"recipient":{
  			"id":senderID
  		},
  		"message":{
  			"text": message
  		}
	}
	requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + pageAccessToken, headers=headers, data=json.dumps(payload))

def decipherChoice(value):
	myList = []
	while (value > 0):
		next = value%10
		#print(next)
		myList.append(value%10)
		value = value//10
		#print(value)
	return myList

#send to Subs
def sendToSubscribers(diningHallMenuDict):
	print("Sending to subscribers!!")
	n = 0
	print("Dininghallmenudict: %s" % diningHallMenuDict)

	for key in db.keys():
		#print("size of keys %s" % len(db.keys()))
		#print(db.get(key.decode('utf-8')))
		print("key %s: %s" % (n, key.decode('utf-8')))
		if key.decode('utf-8') != 'diningHallMenuDict' and db.get(key.decode('utf-8')) > 0:
			print("key %s: %s" % (n, key.decode('utf-8')))
			n = n + 1
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
					time.sleep(.25)

		sendMessage(key.decode('utf-8'), "If you would like to edit your selection simply message \"edit\" any time. Additionally, to unsubscribe message \"unsubscribe\" (but we'll be sad to see you go!).")
		sendMessage(key.decode('utf-8'), "----------------------")




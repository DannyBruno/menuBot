

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
def sendToSubscribers():
	print("Sending to subscribers!!")
	n = 0

	for key in db.keys():
		#print("size of keys %s" % len(db.keys()))
		if db.get(key.decode('utf-8')) > 0:
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




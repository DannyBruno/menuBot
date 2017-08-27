

diningHallList = ["Bursley", "East Quad", "Markley", "Mosher-Jordan (Mojo)", "North Quad", "South Quad", "Twigs (Oxford)"]

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


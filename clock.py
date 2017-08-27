import pytz
import os

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from app import pullMenus, diningHallMenuDict, diningHallList, sendToSubscribers





scheduler = BackgroundScheduler()


headers = {
	"Content-Type": "application/json"
}
secret = {
		'secret_key': os.environ['secret_key']
}


@scheduler.scheduled_job('cron', hour=3, minute=21, second=10, timezone=pytz.timezone('US/Eastern'))
def startCaching():
	print("Hmm")
	#request
	payload = {
		'request': 'cache'
	}
	#requests.post(request.url_root + "/request", params=secret, data=json.dumps(payload), headers=headers)

@scheduler.scheduled_job('cron', hour=3, minute=21, second=45, timezone=pytz.timezone('US/Eastern'))
def startSending():
	print("What")
	#request
	payload = {
		'request': 'send'
	}
	#requests.post(request.url_root + "/request", params=secret, data=json.dumps(payload), headers=headers)


scheduler.start()
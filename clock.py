import pytz
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from sending import sendToSubscribers
from caching import pullMenus



diningHallList = ["Bursley", "East Quad", "Markley", "Mosher-Jordan (Mojo)", "North Quad", "South Quad", "Twigs (Oxford)"]


diningHallMenuDict = {}



'''___Testing___'''
'''
import redis


db = redis.from_url('redis://h:p3116b29cf75492a50fe130ffeb19d111fe87d4b0daea9440e235fec5a5f14300@ec2-34-224-49-43.compute-1.amazonaws.com:45779')

db.set('1458256307549428', 3456)

pullMenus(diningHallMenuDict, diningHallList)

time.sleep(5)

sendToSubscribers(diningHallMenuDict)
'''


'''____Schedulers____'''
scheduler = BackgroundScheduler()

print("1")
scheduler.add_job(pullMenus, 'cron', [diningHallMenuDict, diningHallList], hour=20, minute=26, second=10, timezone=pytz.timezone('US/Eastern'))
	
print("2")
scheduler.add_job(sendToSubscribers, 'cron', [diningHallMenuDict], hour=20, minute=26, second=45, timezone=pytz.timezone('US/Eastern'))

print("3")
scheduler.start()
print("Scheduler started")
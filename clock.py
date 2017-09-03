import pytz
import os
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, request
from rq import Queue
from worker import conn
from sending import sendToSubscribers
from caching import pullMenus




diningHallList = ["Bursley", "East Quad", "Markley", "Mosher-Jordan (Mojo)", "North Quad", "South Quad", "Twigs (Oxford)"]


diningHallMenuDict = {}

q = Queue(connection=conn)



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
scheduler = BlockingScheduler()


print("Job 1 Added..")
#scheduler.add_job(pullMenus, 'cron', [diningHallMenuDict, diningHallList], hour=20, minute=26, second=10, timezone=pytz.timezone('US/Eastern'))
@scheduler.scheduled_job('cron', [diningHallMenuDict, diningHallList], hour=18, minute=48, second=10, timezone=pytz.timezone('US/Eastern'))
def spinCacheWorker(diningHallMenuDict, diningHallList):
	diningHallMenuDict = q.enqueue(pullMenus, diningHallMenuDict, diningHallList)
	@scheduler.scheduled_job('cron', [diningHallMenuDict], hour=18, minute=48, second=45, timezone=pytz.timezone('US/Eastern'))
	def spinSendWorker(diningHallMenuDict):
		q.enqueue(sendToSubscribers, diningHallMenuDict)

'''
print("Job 2 added..")
#scheduler.add_job(sendToSubscribers, 'cron', [diningHallMenuDict], hour=20, minute=26, second=45, timezone=pytz.timezone('US/Eastern'))
@scheduler.scheduled_job('cron', [diningHallMenuDict], hour=18, minute=43, second=45, timezone=pytz.timezone('US/Eastern'))
def spinSendWorker(diningHallMenuDict):
	q.enqueue(sendToSubscribers, diningHallMenuDict)
'''
scheduler.start()
print("Scheduler started")
print("~~Done~~")





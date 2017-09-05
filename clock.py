import pytz
import os
import time
import redis
import pickle

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, request
from rq import Queue
from worker import conn
from sending import sendToSubscribers
from caching import pullMenus



dictDb = redis.from_url(os.environ['REDIS_URL'], db= 0)
#dictDb = redis.from_url('redis://h:p3116b29cf75492a50fe130ffeb19d111fe87d4b0daea9440e235fec5a5f14300@ec2-34-224-49-43.compute-1.amazonaws.com:45779', db= 0)


q = Queue(connection=conn)



'''___Testing___'''
'''


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
@scheduler.scheduled_job('cron', hour=19, minute=10, second=10, timezone=pytz.timezone('US/Eastern'))
def spinCacheWorker():
	result = q.enqueue(pullMenus)

print("Job 2 added..")
#scheduler.add_job(sendToSubscribers, 'cron', [diningHallMenuDict], hour=20, minute=26, second=45, timezone=pytz.timezone('US/Eastern'))
@scheduler.scheduled_job('cron', hour=19, minute=10, second=45, timezone=pytz.timezone('US/Eastern'))
def spinSendWorker():
	result = q.enqueue(sendToSubscribers, pickle.loads(dictDb.get("diningHallMenuDict")))

scheduler.start()
print("Scheduler started")
print("~~Done~~")





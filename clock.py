import pytz
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from sending import sendToSubscribers
from caching import pullMenus



diningHallList = ["Bursley", "East Quad", "Markley", "Mosher-Jordan (Mojo)", "North Quad", "South Quad", "Twigs (Oxford)"]


diningHallMenuDict = {}




'''____Schedulers____'''
scheduler = BackgroundScheduler()


scheduler.add_job(pullMenus, 'cron', [diningHallMenuDict, diningHallList], hour=3, minute=21, second=10, timezone=pytz.timezone('US/Eastern'))
	

scheduler.add_job(sendToSubscribers, 'cron', hour=3, minute=21, second=45, timezone=pytz.timezone('US/Eastern'))


scheduler.start()
print("Scheduler started")
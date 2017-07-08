import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/webhook', methods=['GET'])
def verify():
	if request.args["hub.mode"] == "subscribe":
		if not request.args["hub.verify_token"] == 'verifyMe':
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200

'''
@app.route('/webhook', methods=['POST'])
def webhook():
	if method == 'GET':
'''


if __name__ == '__main__':
	app.run()

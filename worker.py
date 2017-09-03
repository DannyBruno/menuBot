import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

conn = redis.from_url('redis://h:p3116b29cf75492a50fe130ffeb19d111fe87d4b0daea9440e235fec5a5f14300@ec2-34-224-49-43.compute-1.amazonaws.com:45779', db= 1)
#conn = redis.from_url(os.environ['REDIS_URL'], db= 1)


if __name__ == '__main__':
	with Connection(conn):
		worker = Worker(map(Queue, listen))
		worker.work()
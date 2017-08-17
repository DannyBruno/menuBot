import os
basedir = os.path.abspath(os.path.dirname(__file__))


'''______FILL_IN_IF_NEEDED______'''
class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    PAGE_ACCESS_TOKEN = 'EAAB6sqmI7uwBAOk4EZBGAgB67ZA40ziA7T5r82TUiXZAFnacYHcuK5KRFsVHy7le7SrUzmCfJQVamZBArsAzTcdGSeUzrUNPTh8V3PeIuVfKto2f43eqK4aj2Mk72J95e1HKj9SHVerm3ZAG20dT9SPAGO8b3u6ZCoZBv8tcuQHmhvyYH0EqiH6'
    REDIS_URL = 'redis://h:p3116b29cf75492a50fe130ffeb19d111fe87d4b0daea9440e235fec5a5f14300@ec2-34-224-49-43.compute-1.amazonaws.com:45779'


    


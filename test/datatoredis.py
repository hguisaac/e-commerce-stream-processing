from yaml import load, Loader
from textblob import TextBlob
import redis
import os
import pandas as pd
conf = load(open('config.yaml'), Loader=Loader)



rconf = conf["servers"]["redis"]
rconn = redis.Redis(host=rconf["host"], port=rconf["port"], db=1)
# print(conf["actions"])

# countries = pd.read_csv("data/countries.csv")
# comments = pd.read_csv("data/comments.csv")
# print(countries)

f = pd.read_csv("data/toto.csv")
f["reviews.title"].to_csv(r"data/out.csv")
# rcon.set('foo', 'bar')
# for i in range(1000):
    # rconn.set(i, countries["countries"][i])
# compression_opts = dict(method='zip', archive_name='out.csv')   
# mb["reviews.title"].to_csv('oute.zip', index=False, compression=compression_opts)
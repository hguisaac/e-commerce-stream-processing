import nltk
# from textblob import TextBlob
# import redis
# from yaml import load, Loader
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

# conf = load(open('config.yaml'), Loader=Loader)

# rconf = conf["servers"]["redis"]
# rconn = redis.Redis(host=rconf["host"], port=rconf["port"], db=3)
sia = SentimentIntensityAnalyzer()

def get_humour(message):
    if message != None:
        sentiment = sia.polarity_scores(message) # .decode()
        if sentiment['compound'] > 0.0:
            return "GOOD"
        elif sentiment['compound'] < 0.0:
            return "BAD"
        else:
            return "NEUTRAL"
    return "NEUTRAL"





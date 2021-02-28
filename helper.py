from math import floor
from random import random, choice, choices, randint
from datetime import datetime
from scipy.stats import gamma, uniform
from os import path
from yaml import load, Loader
import redis
import pprint 

# TODO: 

# ANSI Colors 
W  = "\033[0m"  # white 
R  = "\033[31m" # red
G  = "\033[32m" # green
O  = "\033[33m" # orange
B  = "\033[34m" # blue
P  = "\033[35m" # purple
C  = "\033[36m" # cyan
M  = "\033[35m" # magenta

conf = load(open('config.yaml'), Loader=Loader)

# load constants from config.yaml file

ACTIONS                 = conf["actions"]["names"]
DEBIT_CARDS             = conf["cards"]["names"]
UID_LIMIT               = conf["limit"]["users"]
AID_LIMIT               = conf["limit"]["articles"]
APP_NAME                = conf["app"]
PROMOTIONS              = conf["promotions"]["names"]
KAFKA_BOOTSTRAP_SERVERS = ":".join(conf["servers"]["kafka"].values())
JARS_DIR                = path.join(path.abspath("") + "/" + conf["jars"])
REDIS_SERVER            = conf["servers"]["redis"]
METRICS_SOCKETS         = conf["servers"]["graphing_sockets"]



class Event:
    def __init__(self):
        '''
            :params        uid: user identificator
            :params        aid: article identificator
            :params created_at: event emitted time
            :params     action: bind to kafka topic 
            
        '''
        # action has the same name as the name of the class from where 
        # it (as attribut) is initiated
        self.action     = self.__class__.__name__.lower()
        self.uid        = Generator.get_gamma(UID_LIMIT)             
        self.aid        = Generator.get_gamma(AID_LIMIT)          
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        
    def __str__(self):
        return f"( action={self.action}, time={self.created_at}, uid={self.uid}, aid={self.aid}"
        

class Purchasse(Event):
    def __init__(self):
        '''
            :params     number: number of article the user is about to buy
            :params  promotion: promotion that the user is using for this purchasse
            :params       card: card used by the current for purchassing

        '''
        super().__init__()
        # self.action     = "purchasse"
        self.number     = Generator.get_quantity()
        self.promotion  = Generator.get_promo()
        self.card  = Generator.get_card()

    def __str__(self):
        return super().__str__() + f", promotion={self.promotion}, card={self.card}, number={self.number} )"


class Basket(Event):
    def __init__(self):
        '''
            :params     number: number of article the user is about to buy
            :params  promotion: promotion that the user is using for this purchasse
        
        '''
        super().__init__()
        self.number     = Generator.get_quantity()
        self.promotion  = Generator.get_promo()

    def __str__(self):
        return super().__str__() + f", promotion={self.promotion}, number={self.number}" + f" )"

class Comment(Event):
    def __init__(self):
        super().__init__()
        # get_message returns a comment about the article self.aid
        self.body       = Generator.get_message()
        self.promotion  = Generator.get_promo()

    def __str__(self):
        return super().__str__() + f", body={self.body}" + f" )"

    def __str__(self):
        return super().__str__() + f", body={self.body}" + f" )"

class Bookmark(Event):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return super().__str__() + f" )"


class Click(Event):
    def __init__(self):
        super().__init__()
        # self.body       = Generator.get_message() 
        # self.promotion  = Generator.get_promo()

    def __str__(self):
        return super().__str__() + f" )"

class Generator:
    @staticmethod
    def get_gamma(lim):
        return int(gamma.rvs(a=5)/12*lim)

    @staticmethod  
    def get_promo():      
        return choices(PROMOTIONS,  weights=conf["promotions"]["dist"], k=1)[0]
    
    @staticmethod
    def get_quantity():
        # generate the quantity of article the user is about to buy or 
        # have bought regarding some action, as choice used uniform distribution
        if conf["quantities"]["static"] == False:
            liminf = len(conf["quantities"]["values"])
            conf["quantities"]["values"].pop(liminf-1) # pop out the last element
            conf["quantities"]["values"].append(randint(liminf,conf["quantities"]["limsup"]))
        return choices(conf["quantities"]["values"], weights=conf["quantities"]["dist"], k=1)[0]

    @staticmethod
    def get_message():
        rconn = redis.Redis(
            host=REDIS_SERVER["host"], 
            port=REDIS_SERVER["port"], 
            db=REDIS_SERVER["db"]
        )
        body = rconn.get(randint(1,conf["data_comment"]["size"]))
        if body != None:
            body = body.decode('ASCII')
        return body
        
    @staticmethod
    def get_card():
        return choices(DEBIT_CARDS, weights=conf["cards"]["dist"], k=1)[0]

    @staticmethod
    def emit():
        # map each action to an event with the same name
        events = list(
            map(lambda action: eval(action), ACTIONS)
        )
        event = choices(events, weights=conf["actions"]["dist"], k=1)[0]()
        return event


# ----------------------------------------------------------------------------
# Further informations
# ----------------------------------------------------------------------------
# Random fonctions can be manipulated/reseed using seed provided by the library
# from where it has been picked. Random function use a sequence variable in memory
# to keep track of (already) returned  or not values.

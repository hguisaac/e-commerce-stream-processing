from kafka import KafkaProducer
from datetime import datetime
from json import dumps
from random import random, choice
from helper import Purchasse,  Bookmark, Comment, Basket, Click, Generator, APP_NAME, KAFKA_BOOTSTRAP_SERVERS, ACTIONS, C, W
from time import sleep
from sys import stdout

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, 
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


(
   lambda name, rule_size: stdout.write(
      f"{'='*(len(name)+rule_size)}"
      +"\n"
      +f"|{name:^{len(name)+(rule_size-2)}}|"
      +"\n"
      +f"{'='*(len(name)+rule_size)}"
      +"\n"
   )
)(APP_NAME, 10)


def produce_event_forever():
    while True:
        event = Generator.emit() 
        producer.send(topic=event.action, value=event.__dict__)
        produce_event_forever.count += 1
        print(event) 
        print("event_count", C, "%", produce_event_forever.count, W)
        # wait a few milliseconds
        sleep(random()) 
        if produce_event_forever.count == 200:
            sleep(100000)
    
produce_event_forever.count = 0
produce_event_forever()
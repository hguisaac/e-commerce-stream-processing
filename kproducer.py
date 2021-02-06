from kafka import KafkaProducer
from datetime import datetime
from json import dumps
from random import random, choice
from helper import Purchasse,  Bookmark, Comment, Basket, Click, Generator, APP_NAME, KAFKA_BOOTSTRAP_SERVERS, ACTIONS
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

count = 1
while True:
   
    event = Generator.emit() 
    # event.__dict__ acts as var(event)
    producer.send(topic=event.action, value=event.__dict__)
    count = count + 1   
    print(event) 
    sleep(random()) 
    print("NUMBER::",count)
    

from kafka import KafkaConsumer
from helper import KAFKA_BOOTSTRAP_SERVERS, W, R, P, M, G
from collections import namedtuple
from functools import reduce
from multiprocessing import Process
from threading import Thread
from time import sleep
import json
import sys
import os
import re
import pickle
import socket



def create_client_sckt(socket_address=("127.0.1.1", 33333)):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect(socket_address)
    return sckt

def send_data(data:list):
    print(send_data.click_sckt)
    send_data.click_sckt.send(pickle.dumps(data))
    pass

send_data.click_sckt = create_client_sckt()

for __ in range(9):
    send_data("re")


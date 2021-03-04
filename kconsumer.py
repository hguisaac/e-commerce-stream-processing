from kafka import KafkaConsumer
from helper import KAFKA_BOOTSTRAP_SERVERS, METRICS_SOCKETS, W, R, P, M, G
from collections import namedtuple
from functools import reduce
from multiprocessing import Process
from threading import Thread
from time import sleep
from yaml import load, Loader
import json
import sys
import os
import re
import pickle
import socket


# load metrics sockets server address


promotion_counts_list = []
most_clicked_article_list = []
most_bookmarked_article_list = []
article_bad_comment_count_list = []
count_size_to_send = 3
# will use count_size_to_send*2 in the condition 


def sckt_connect(sckt_addr:dict):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect(tuple(sckt_addr.values()))
    return sckt


click_socket_address = ("127.0.1.1", 33333)


sckt = None
def create_client_sckt(socket_address=("127.0.1.1", 33332)):
    # global sckt
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect(socket_address)
    return sckt

def send_data_to_socket_server(data:list):
    pass



def send_data(data:list):
    global sckt
    if sckt == None:
        sckt = create_client_sckt()
    serialized_data = pickle.dumps(data)
    sckt.send(serialized_data)


# send_data.promotion_count_sckt = sckt_connect(METRICS_SOCKETS["metric1"])
# send_data.click_count_sckt = sckt_connect(METRICS_SOCKETS["metric2"])
# send_data.bookmark_count_sckt = sckt_connect(METRICS_SOCKETS["metric3"])
send_data.article_humour_count_sckt = sckt_connect(METRICS_SOCKETS["metric4"])


def get_consumer(topic):
    return (
        KafkaConsumer(
            topic, 
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS], 
            api_version=(0, 10, 1)
        )
    )


def update_promotion_count_cursor_within_socket(
    new_count,
    promotion_counts_list=promotion_counts_list
):
    print("new_count", M, new_count, W)
    some_count_has_been_updated = False
    for line in promotion_counts_list:
        if line[0] == new_count[0] and line[1] == new_count[1]:
            line[2] = new_count[2]
            some_count_has_been_updated = True
            # as were are using update mode in spark we can not 
            # have the same line many times, so we break
            break
    if some_count_has_been_updated == False:
        promotion_counts_list.append(new_count)
    print("After", promotion_counts_list)
    if len(promotion_counts_list) == 2*count_size_to_send:
        first_date = promotion_counts_list[0][0]
        second_date = promotion_counts_list[1][0]
        third_date = promotion_counts_list[2][0]
        is_well_grouped = True
        if first_date != second_date or first_date != third_date:
            is_well_grouped = False
        if is_well_grouped == True:  
            data_to_send = promotion_counts_list[:count_size_to_send]
            data_to_send.sort()
            send_data(data_to_send)
            promotion_counts_list = promotion_counts_list[count_size_to_send:]
        else:
            promotion_counts_list = promotion_counts_list[1:]
    return promotion_counts_list


def update_click_counts_within_socket(
    new_record,
    func=most_bookmarked_article_list
):
    print("update_func says: ", G, new_record, W)
    send_data.click_count_sckt.send(pickle.dumps(new_record))

def update_bookmark_counts_within_socket(
    new_record,
    func=most_bookmarked_article_list
):
    print("update_func says: ", G, new_record, W)
    send_data.bookmark_count_sckt.send(pickle.dumps(new_record)) 

def update_article_humour_counts_within_socket(
    new_record,
    func=promotion_counts_list
):
    print("toto")
    print("update_func says: ", G, new_record, W)
    send_data.article_humour_count_sckt.send(pickle.dumps(new_record)) 



def read_and_load_computation_into_global_var(
    global_variable_name:str, 
    source_topic, 
    update_func
):
    
    # globar_variable_name is the name of the global list
    # which will be used for graphing but as string
    consumer = get_consumer(source_topic)
    # then real_global_variable will be a global list ie python object 
    # having the name global_var
    real_global_variable = globals()[global_variable_name]
    
    for msg in consumer:
        try:
            value = json.loads(msg.value.decode())
            start_match = re.search("\d\d:\d\d:\d\d", value["win_start"])
            end_match = re.search("\d\d:\d\d:\d\d", value["win_end"])
            if start_match == None:
                start_match = re.search("\d\d:\d\d:\d\d", value["win_start"])
            if end_match == None:
                end_match = re.search("\d\d:\d\d:\d\d", value["win_start"])

            assert start_match != None
            assert end_match != None

            time_win = (
                value["win_start"][start_match.start():start_match.end()]
                +
                "-"
                +
                value["win_end"][end_match.start():end_match.end()]
            )

            values_list = list(value.values())[2:]
            values_list.insert(0, time_win)

            real_global_variable = update_func(
                values_list,
                real_global_variable
            )
            
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(R, exception, fname, "line", exc_tb.tb_lineno, W)
            continue
        print("______________________________________")
        print("______________________________________")
        # print(R, promotion_counts_points, W)



promotion_counts_thread = Thread(
    target=read_and_load_computation_into_global_var,
    args=["promotion_counts_list"],
    kwargs={
        "source_topic":"purchasse_sink",
        "update_func":update_promotion_count_cursor_within_socket
    }
)


click_counts_thread = Thread(
    target=read_and_load_computation_into_global_var,
    args=["most_clicked_article_list"],
    kwargs={
        "source_topic":"click_sink",
        "update_func":update_click_counts_within_socket
    }
)


bookmark_counts_thread = Thread(
    target=read_and_load_computation_into_global_var,
    args=["most_bookmarked_article_list"],
    kwargs={
        "source_topic":"bookmark_sink",
        "update_func":update_bookmark_counts_within_socket
    }
)

article_bad_comment_count_thread = Thread(
    target=read_and_load_computation_into_global_var,
    args=["article_bad_comment_count_list"],
    kwargs={
        "source_topic":"comment_sink",
        "update_func":update_article_humour_counts_within_socket
    }
)

print("starting threads")
promotion_counts_thread.start()
# article_bad_comment_count_thread.start()
# bookmark_counts_thread.start()
# click_counts_thread.start()

print("joining threads")
promotion_counts_thread.join()
# article_bad_comment_count_thread.join()
# bookmark_counts_thread.join()
# click_counts_thread.join()


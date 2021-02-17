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

promotion_counts_list = []
count_size_to_send = 3
# will use count_size_to_send*2 in the condition 

sckt = None
def create_client_sckt(sckt_socket=("127.0.1.1", 33332)):
    # global sckt
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.connect(sckt_socket)
    return sckt

def send_data(data:list):
    global sckt
    if sckt == None:
        sckt = create_client_sckt()
    serialized_data = pickle.dumps(data)
    sckt.send(serialized_data)



def get_consumer(topic):
    return (
        KafkaConsumer(
            topic, 
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS], 
            api_version=(0, 10, 1)
        )
    )



def update_promotion_count(
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


def read_and_load_computation_into_global_var(
    global_variable_name:str, 
    source_topic, 
    update_data_func
):
    
    # globar_variable_name is the name of the global 
    # list whichwill be used for graphing but as string
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

            # we don't want to go back
            
            values_list = list(value.values())[2:]
            values_list.insert(0, time_win)

            real_global_variable = update_data_func(
                values_list,
                real_global_variable
            )
        
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(R, exception, fname, "line", exc_tb.tb_lineno, W)
            continue
        # actualize_printing_cursor(real_global_variable)
        print("______________________________________")
        print("______________________________________")
        # print(R, promotion_c31ounts_points, W)

    
promotion_counts_thread = Thread(
    target=read_and_load_computation_into_global_var,
    args=["promotion_counts_list"],
    kwargs={
        "source_topic":"purchasse_sink",
        "update_data_func":update_promotion_count
    }
)

# promotion_counts_plot_thread = Thread(
#     target=promotion_counts_plot
# )

print("starting thread")
promotion_counts_thread.start()
promotion_counts_thread.join()
print("after starting thread")

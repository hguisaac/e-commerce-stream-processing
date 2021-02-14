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




# TODO: use args, kwars in Process construtor instead of anonymous fonction
# stacks to graph
most_bably_commented_article_points = []
promotion_counts_points = []
most_clicked_article_points = []
most_bookmarked_article_points = []


most_bably_commented_article_list = []
promotion_counts_list = []
most_clicked_article_list = []
most_bookmarked_article_list = []


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
        
    return promotion_counts_list



def actualize_printing_cursor(some_list, size=12):
    some_list_size = len(some_list)
    if some_list_size > size:
        del some_list[:some_list_size-size]
    return some_list

def get_consumer(topic):
    return (
        KafkaConsumer(
            topic, 
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS], 
            api_version=(0, 10, 1)
        )
    )

# un processus peut avoir deux thread 
# donc : je peux utiliser un thread 

def promotion_counts_plot():
    global promotion_counts_list
    while True:
        print("Grapher", G, promotion_counts_list, W)
    pass
    


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

            assert(start_match != None)
            assert(end_match != None)

            time_win = (
                value["win_start"][start_match.start():start_match.end()]
                +
                "-"
                +
                value["win_end"][end_match.start():end_match.end()]
            )

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
        # print(R, promotion_counts_points, W)

# parallelization

# most_bably_commented_article_process = Process(
#     target=read_and_load_computation_into_global_var,
#     args=["most_bably_commented_article_points"],
#     kwargs={"source_topic":"comment_sink"}
# )

promotion_counts_thread = Thread(
    target=read_and_load_computation_into_global_var,
    args=["promotion_counts_list"],
    kwargs={
        "source_topic":"purchasse_sink",
        "update_data_func":update_promotion_count
    }
)

promotion_counts_plot_thread = Thread(
    target=promotion_counts_plot
)


# most_clicked_article_process = Process(
#     target=read_and_load_computation_into_global_var,
#     args=["most_clicked_article_points"],
#     kwargs={"source_topic":"click_sink"}
# )

# most_bookmarked_article_process = Process(
#     target=read_and_load_computation_into_global_var,
#     args=["most_bookmarked_article_points"],
#     kwargs={"source_topic":"bookmark_sink"}
# )
        
# plot_process = Process(
#     target=live_grouped_bar_plot
# )

# plot_process.start()
# plot_process.join()

# # start processes
# most_bably_commented_article_process.start()
promotion_counts_thread.start()
# most_clicked_article_process.start()
# most_bookmarked_article_process.start()

# # wait to the main process to complete 
# most_bably_commented_article_process.join()
promotion_counts_plot_thread.start()
promotion_counts_thread.join()
promotion_counts_plot_thread.join()

# most_clicked_article_process.join()
# most_bookmarked_article_process.join()


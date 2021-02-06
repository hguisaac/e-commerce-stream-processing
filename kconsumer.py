from kafka import KafkaConsumer
from helper import KAFKA_BOOTSTRAP_SERVERS, W, R
from collections import namedtuple
from functools import reduce
from multiprocessing import Process
import json


# TODO: use args, kwars in Process construtor instead of anonymous fonction
# stacks to graph
most_bably_commented_article_points = []
promotion_counts_points = []
most_clicked_article_points = []
most_bookmarked_article_points = []

def actualize_printing_cursor(some_list, size=4):
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



def read_and_load_computation_into_global_var(global_var_name:str, source_topic):
    # globar_var is the name of the global list which
    # will be used for graphing but as string
    Point = None
    consumer = get_consumer(source_topic)
    # then real_global_var will be a global list ie python object 
    # having the name global_var
    real_global_var = globals()[global_var_name]
    isset_attributes = False
    for msg in consumer:
        try:
            value = json.loads(msg.value.decode())
            if isset_attributes is False:
                # create a namedtuple with value.keys()
                Point = namedtuple(
                    "Point", 
                    reduce(
                        lambda a, b: a + " " + b,
                        value.keys()
                    )
                )
                isset_attributes = True
            
        except Exception as exception:
            print(R,exception,W)
            # the presence of the instruction continue is very important
            continue
        # create a Point namedtuples object using value.values()
        # and append this object into related global variable
        real_global_var.append(
                Point(
                    *(value.values())
                )
            )
        actualize_printing_cursor(real_global_var)
        print(real_global_var)

# make each metric a process and  
# make them to run asynchronously

most_bably_commented_article_process = Process(
    target=read_and_load_computation_into_global_var,
    args=["most_bably_commented_article_points"],
    kwargs={"source_topic":"comment_sink"}
)

promotion_counts_process = Process(
    target=read_and_load_computation_into_global_var,
    args=["promotion_counts_points"],
    kwargs={"source_topic":"purchasse_sink"}
)

most_clicked_article_process = Process(
    target=read_and_load_computation_into_global_var,
    args=["most_clicked_article_points"],
    kwargs={"source_topic":"click_sink"}
)

most_bookmarked_article_process = Process(
    target=read_and_load_computation_into_global_var,
    args=["most_bookmarked_article_points"],
    kwargs={"source_topic":"bookmark_sink"}
)

# start processes
most_bably_commented_article_process.start()
promotion_counts_process.start()
most_clicked_article_process.start()
most_bookmarked_article_process.start()

# wait to the main process to complete 
most_bably_commented_article_process.join()
promotion_counts_process.join()
most_clicked_article_process.join()
most_bookmarked_article_process.join()


    
    


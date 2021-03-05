from helper import KAFKA_BOOTSTRAP_SERVERS, ACTIONS, JARS_DIR, Purchasse,  Bookmark, Comment, Basket, Click, W, R
from nlp import get_humour
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from multiprocessing import Process
from IPython import display
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas
import os

os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_DRIVER_PYTHON"]="/usr/bin/python3"

# manage duplicate actions in the list ACTIONS
KAFKA_TOPICS = (
    list(
        set(
            map(lambda action: action, ACTIONS)
        )
    )
)

# include spark_sql_kafka.jar 
# include kafka_client.jar
JAR_FILES = (
    ""
    + "file://" 
    + JARS_DIR
    + "spark-sql-kafka-0-10_2.11-2.4.0.jar,file://"
    + JARS_DIR
    + "kafka-clients-1.1.1.jar"
)

SOURCE = "kafka"
SINK = "kafka"
CHECKPOINT_LOCATION = "vendor/spark/checkpoint"

COMMENT_HUMOURS= {
    "bad":"BAD",
    "good":"GOOD",
    "neutral":"NEUTRAL"
}

ssession = ( 
    SparkSession.builder 
                .master('local[2]') 
                .config("spark.jars", JAR_FILES) 
                .config("spark.executor.extraClassPath", JAR_FILES) 
                .config("spark.executor.extraLibrary", JAR_FILES) 
                .config("spark.driver.extraClassPath", JAR_FILES) 
                .appName("Spark Memo Demo") 
                .getOrCreate()
)

ssession.sparkContext.setLogLevel("ERROR")


def get_dfstream(topic, source=SOURCE):
    # source is the parameter to pass to format method 
    return (
        ssession.readStream
                .format(source)
                .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
                .option("subscribe", topic)
                .load()
    )

def to_json_string(df):
    # convert native dataframe to json string
    return (
        df.withColumn(
            "value",
            to_json(
                struct([df[x] for x in df.columns])
            )
        )
    )

def get_formatted_dfstream(source_topic, source=SOURCE):
    # source is the parameter to pass to format method 
   
    df_stream = ( 
        ssession.readStream
                .format(source)
                .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
                .option("failOnDataLoss", "false")
                .option("subscribe", source_topic)
                .load()
    )
    
    df_stream.printSchema()
    df_stream = (
        df_stream
        .selectExpr(
            "CAST(value AS STRING)", 
            "timestamp"
        )
    )
    # dynamically create objet from class having the same topic name
    obj = eval(
        source_topic.capitalize()
    )()

    attributes = list(
        obj
        .__dict__
        .keys()
    )

    del obj

    data_schema = StructType()
    for attr in attributes:
        data_schema = data_schema.add(attr, StringType())

    return (
        df_stream
        .select(
            from_json(
                col("value"), data_schema
            ).alias("event_value"), 
            "timestamp"
        )
    )
    

def write_computation(df_stream, sink_topic, processing_time="1 seconds", sink=SINK):
    df_stream = to_json_string(df_stream)
    tmp_df = (
        df_stream.writeStream
                 .format(SINK)
                 .trigger(processingTime=processing_time)
                 .outputMode("update")
                 .option("checkpointLocation", CHECKPOINT_LOCATION)
    )
    if SINK == "kafka":
        tmp_df = (
            tmp_df.option("kafka.bootstrap.servers",KAFKA_BOOTSTRAP_SERVERS)
                  .option("topic", sink_topic)
        )
    return tmp_df.start()

def compute_promotion_counts (
    watermark_time="2 hours", 
    win_column=None, 
    win_size="2 minutes",  
    win_sliding="2 minutes", 
    # win_start < win_sliding
    win_start="1 minutes"
):
    source_topic = "purchasse"
    df = get_formatted_dfstream(source_topic=source_topic, source=SOURCE)
    df = (
        df
        .withWatermark("timestamp", watermark_time)
        .groupBy(
            # window(col_time, win_time, sliding_time, start_time)
            # start_time must be less than sliding_time
            window(df.timestamp, win_size, win_sliding, win_start),
            df.event_value.promotion
        )
        .count()      
    )

    # df.printSchema()
    # root
    # |-- window: struct (nullable = false)
    # |    |-- start: timestamp (nullable = true)
    # |    |-- end: timestamp (nullable = true)
    # |-- event_value[promotion]: string (nullable = true)
    # |-- count: long (nullable = false)

    # rename nested columns start and end
    df = (
        df
        .select(
            col("window.start").alias("win_start"),
            col("window.end").alias("win_end"),
            col("event_value[promotion]").alias("promo"),
            col("count")
        )
    )

    # df.printSchema()
    # root
    # |-- win_start: timestamp (nullable = true)
    # |-- win_end: timestamp (nullable = true)
    # |-- promo: string (nullable = true)
    # |-- count: long (nullable = false)

    return write_computation(df, processing_time="2 seconds", sink=SINK, sink_topic=source_topic+"_sink")

def compute_click_counts (
    watermark_time="2 hours", 
    win_column=None, 
    win_size="2 minutes",  
    win_sliding="2 minutes", 
    win_start="1 minutes"
):
    source_topic = "click"
    df = get_formatted_dfstream(source_topic=source_topic, source=SOURCE)
    df = (
        df
        .withWatermark("timestamp", watermark_time)
        .groupBy(
            window(df.timestamp, win_size, win_sliding, win_start),
            df.event_value.aid
        )
        .count()
    )
    
    df = (
        df
        .select(
            col("window.start").alias("win_start"),
            col("window.end").alias("win_end"),
            col("event_value[aid]").alias("article_id"),
            col("count")
        )
    )
    
    # df.printSchema()
    # root
    # |-- win_start: timestamp (nullable = true)
    # |-- win_end: timestamp (nullable = true)
    # |-- promo: string (nullable = true)
    # |-- count: long (nullable = false)

    return write_computation(df, processing_time="2 seconds", sink=SINK, sink_topic=source_topic+"_sink")


def compute_bookmark_counts (
    watermark_time="2 hours", 
    win_column=None, 
    win_size="2 minutes",  
    win_sliding="2 minutes", 
    win_start="1 minutes"
):
    source_topic = "bookmark"
    df = get_formatted_dfstream(source_topic=source_topic, source=SOURCE)
    df = (
        df
        .withWatermark("timestamp", watermark_time)
        .groupBy(
            window(df.timestamp, win_size, win_sliding, win_start),
            df.event_value.aid
        ).count()
    )
    # 
    df.printSchema()
    # root
    # |-- window: struct (nullable = false)BAD
    # |    |-- start: timestamp (nullable = true)
    # |    |-- end: timestamp (nullable = true)
    # |-- event_value[aid]: string (nullable = true)

    df = (
        df
        .select(
            col("window.start").alias("win_start"),
            col("window.end").alias("win_end"),
            col("event_value[aid]").alias("article_id"),
            col("count")
        )
    )
    
    return write_computation(df, processing_time="2 seconds", sink=SINK, sink_topic=source_topic+"_sink")

def article_humour_counts (
    watermark_time="2 hours", 
    win_column=None, 
    win_size="2 hours",  
    win_sliding="2 hours", 
    win_start="1 hours"
):
    source_topic = "comment"
    df = get_formatted_dfstream(source_topic=source_topic, source=SOURCE)
    df = (
        df
        .withColumn("customer_humour", 
                    (
                        udf(get_humour, StringType())
                    )(df.event_value.body)
        )
    )
    
    df = (
        df
        .withWatermark("timestamp", watermark_time)
        .groupBy(
            window(df.timestamp, win_size, win_sliding, win_start),
            df.event_value.aid,
            "customer_humour"
        ).count()      
    )

    # root
    # |-- window: struct (nullable = false)
    # |    |-- start: timestamp (nullable = true)
    # |    |-- end: timestamp (nullable = true)
    # |-- customer_humour: string (nullable = true)
    # |-- count: long (nullable = false)

    # rename nested columns start and end
    df = (
        df
        .select(
            col("window.start").alias("win_start"),
            col("window.end").alias("win_end"),
            col("customer_humour").alias("humour"),
            col("event_value[aid]").alias("article_id"),
            col("count")
        )
        # .where(col("customer_humour") == COMMENT_HUMOURS["bad"])
    )

    return write_computation(df, processing_time="2 seconds", sink=SINK, sink_topic=source_topic+"_sink")


# compute_promotion_counts_process = Process(
#     target=(
#         lambda:compute_promotion_counts().awaitTermination()
#     )
# )

# compute_click_counts_process = Process(
#     target=(
#         lambda:compute_click_counts().awaitTermination()
#     )
# )

# compute_bookmark_counts_process = Process(
#     target=(
#         lambda:compute_bookmark_counts().awaitTermination()   
#     )
# )

# article_humour_counts_process = Process(
#     target=(
#         lambda:article_humour_counts().awaitTermination()
#     )
# )


# start processes
# compute_promotion_counts_process.start()
# compute_click_counts_process.start()
# compute_bookmark_counts_process.start()
# article_humour_counts_process.start()

# 
# compute_promotion_counts_process.join()
# compute_click_counts_process.join()
# compute_bookmark_counts_process.join()
# article_humour_counts_process.join()



# compute_promotion_counts().awaitTermination()
# compute_click_counts().awaitTermination()
compute_bookmark_counts().awaitTermination()
# article_humour_counts().awaitTermination()

# ssession.streams.awaitAnyTermination()
#-*- coding: utf-8 -*-
import os
os.system('chcp 65001')

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# dataDirectory="data_to_streaming/"

# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "TwitterStreaming")
ssc = StreamingContext(sc, 5)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines = ssc.socketTextStream("localhost", 9999)

# Split each line into words
words = lines.flatMap(lambda line: line.split(" "))

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
wordCounts.pprint(num=100)

# run
# run Twitter_streamer.py
# %SPARK_HOME%/bin/spark-submit Tweets_processing.py localhost 9999
ssc.start()
ssc.awaitTermination()
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 03:44:48 2019

@author: Tochukwu
"""
import threading
import logging
import time
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer, KafkaProducer

''' The four lines of code below is for creation of the kafka topic "interswitch_topic"''' 
admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id='test')
topic_list = []
topic_list.append(NewTopic(name="interswitch_topic", num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)
class Producer(threading.Thread):
    daemon = True
    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        while True:
            producer.send('interswitch_topic', {"dataObjectID": "test1"})
            producer.send('interswitch_topic', {"dataObjectID": "test2"})
            time.sleep(1)
class Consumer(threading.Thread):
    daemon = True
    def run(self):
        '''initiliaze the consumer '''
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',auto_offset_reset='earliest')
        '''suscribe the consumer to the created topic "interswitch_topic"'''
        consumer.subscribe(['interswitch_topic'])
        for message in consumer:
            print (message)
def main():
    threads = [Producer(),Consumer()]
    for f in threads:
        f.start()
    time.sleep(10)
''' verify that that the code works by logging some information to console''' 
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:' +'%(levelname)s:%(process)d:%(message)s',level=logging.INFO)
    main()

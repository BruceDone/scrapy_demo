# -*- coding: utf-8 -*-
from kafka import KafkaProducer, KafkaConsumer, SimpleConsumer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer('spider', bootstrap_servers='localhost:9092')


def send_message():
    producer.send('spider', 'let us do something new %s' % str(time.time()))


def receive_message():
    # message = consumer.poll(max_records=1)
    # message = next(consumer)
    # print message
    for info in consumer:
        print info


def poll_message():
    message = consumer.poll(20)
    print message


if __name__ == '__main__':
    # receive_message()
    # receive_message()
    # poll_message()
    receive_message()

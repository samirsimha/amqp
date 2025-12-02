#!/usr/bin/env python
import pika

# establish a connection with rabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# creates the hello queue to which the message will be delivered
channel.queue_declare(queue='hello')

# producer sends the message to the exchange (middleman between producer and consumer)
# empty string exchange is the default -- allows us to specify which queue the message should go to as specified by routing_key
channel.basic_publish(
    exchange='', 
    routing_key='hello', 
    body='hello world!'
)
print(" [x] sent 'hello world!'")

connection.close()
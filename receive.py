#!/usr/bin/env python
import pika
import json
import cv2
import os

# establish a connection with rabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check that the queue exists by declaring the queue
channel.queue_declare(queue='hello')

def drain(input, output):
    img = cv2.imread(input)
    if img is None:
        print("error")
    else:
        drained = cv2.bitwise_not(img)
        output_dir = os.path.dirname(output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        success = cv2.imwrite(output, drained)
        if not success:
            print("error")
        print("success")

# define callback function (on message received handler)
def callback(ch, method, properties, body):
    # convert body bytes into string
    text = body.decode("utf-8")
    # convert string into json
    job = json.loads(text)

    inpt = job.get("input")
    outpt = job.get("output")

    drain(inpt, outpt)
    print("success2")
    
    #try:
     #   ch.basic_ack(delivery_tag=method.delivery_tag)
    #except Exception as e:
     #   print("error")


# tell rabbitMQ that callback should be run whenever hello queue receives a message
channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)

# begin waiting for messages to arrive at hello queue
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
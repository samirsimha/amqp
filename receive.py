#!/usr/bin/env python
import pika
import json
import cv2
import os
import numpy as np, math

# establish a connection with rabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check that the queue exists by declaring the queue
channel.queue_declare(queue='hello')

def image_processing(img):
    # image sharpening using openCV
    kernel = np.array([[0, -1,  0],
                       [-1,  5, -1],
                       [0, -1,  0]])
    dst = cv2.filter2D(img, -1, kernel, anchor=(-1, -1), delta=0, borderType=cv2.BORDER_DEFAULT)
    return dst

def sharpening(input, output):
    img = cv2.imread(input)
    if img is None:
        raise Exception(f"Failed to load input image: {input}")
    else:
        drained = image_processing(img)
        output_dir = os.path.dirname(output)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        success = cv2.imwrite(output, drained)
        if not success:
            raise Exception(f"Failed to save output image: {output}")

# define callback function (on message received handler)
def callback(ch, method, properties, body):
    try:
        # convert body bytes into string
        text = body.decode("utf-8")
        # convert string into json
        job = json.loads(text)

        inpt = job.get("input")
        outpt = job.get("output")

        sharpening(inpt, outpt)
        print("success!")
    except Exception as e:
        print(str(e))

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
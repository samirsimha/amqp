#!/usr/bin/env python
import pika
import json

# establish a connection with rabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check that the queue exists by declaring the queue
channel.queue_declare(queue='hello')

# define callback function (on message received handler)
def callback(ch, method, properties, body):
    # convert body bytes into string
    text = body.decode("utf-8")
    # convert string into json
    job = json.loads(text)

    input = job.get("input")
    output = job.get("output")

    print(f"input: {input}, output: {output}")


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
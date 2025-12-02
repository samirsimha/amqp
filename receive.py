#!/usr/bin/env python
import pika

# establish a connection with rabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# check that the queue exists by declaring the queue
channel.queue_declare(queue='hello')

# define callback function (on message received handler)
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

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
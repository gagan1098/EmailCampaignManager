import json
import pika


QUEUE_NAME = "email-campaign"


def send_email(email):
    print(f" [x] Sending email to {email} using SMTP")
    return


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    # validate received data
    try:
        body = json.loads(body)
    except Exception:
        print(" [x] Invalid data received")
        return
    # parse received data to send emails to individual users
    if type(body) is not list:
        print(" [x] Invalid data received")
        return
    for user_data in body:
        email = user_data["email"]
        send_email(email)


def setup_consumer():
    print(" [x] Setup consumer")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
        channel = connection.channel()
        queue_name = f"{QUEUE_NAME}_1"
        channel.queue_declare(queue=queue_name)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as excp:
        print(" [x] cannot connect to RabbitMQ")


if __name__ == "__main__":
    setup_consumer()

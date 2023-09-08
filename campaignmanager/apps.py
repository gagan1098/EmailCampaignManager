import pika
from django.apps import AppConfig


QUEUE_NAME = "email-campaign"


class CampaignmanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campaignmanager'

    @staticmethod
    def setup_consumer():
        print("setup_consumer")

        def callback(ch, method, properties, body):
            print(f" [x] Received {body}")

        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME)

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

            print(" [*] Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()
        except Exception as excp:
            print("cannot connect to RabbitMQ")

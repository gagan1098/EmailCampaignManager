import json
import pika
from django.http import HttpResponse
from campaignmanager.consumer import QUEUE_NAME
from usermanager.views import generate_server_error_response
from usermanager.models import User
from usermanager.views import generate_resource_not_found_response


QUERY_LIMIT = 1


def publish_message(message, routing_key):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_publish(exchange="", routing_key=routing_key, body=message)
        print(f" [x] Sent {message}")
        connection.close()
    except Exception as excp:
        print(excp)
        raise Exception("error pushing message")


def index(request):
    if request.method == "POST":
        try:
            handle_campaign_request()
        except Exception as excp:
            return generate_server_error_response(str(excp))
        return HttpResponse(json.dumps({"status": "success"}))
    else:
        raise generate_resource_not_found_response("method not allowed")


def handle_campaign_request():
    # collect user data
    try:
        users = User.objects.all().filter(active=1)
    except Exception:
        return generate_server_error_response("DB error")
    # publish message to queues using pagination
    count = users.count()
    offset = 0
    queue_number = 1
    while offset + QUERY_LIMIT <= count:
        body = [
            {"email": user.email}
            for user in users[offset:offset+QUERY_LIMIT]
        ]
        routing_key = f"{QUEUE_NAME}_{queue_number % 5}"
        publish_message(json.dumps(body), routing_key)
        offset += QUERY_LIMIT
        queue_number += 1

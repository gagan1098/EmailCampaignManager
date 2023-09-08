import json
import pika
from django.http import HttpResponse
from campaignmanager.apps import QUEUE_NAME
from usermanager.views import generate_server_error_response
from usermanager.models import User
from usermanager.views import generate_resource_not_found_response


def publish_message(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=message)
        print(f" [x] Sent {message}")
        connection.close()
    except Exception:
        raise Exception("error pushing message")


def index(request):
    if request.method == "POST":
        try:
            handle_campaign_request(request)
        except Exception as excp:
            return generate_server_error_response(str(excp))
        return HttpResponse(json.dumps({"status": "success"}))
    else:
        raise generate_resource_not_found_response("method not allowed")


def handle_campaign_request(request):
    queue_message = []
    users = User.objects.all().filter(active=1)
    for user in users:
        queue_message.append({"email": user.email})
    return publish_message(queue_message)

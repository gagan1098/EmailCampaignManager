import datetime
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseServerError
from django.utils import timezone

from .models import User


def generate_success_response(message):
    return HttpResponse(json.dumps({"status": "success", "message": message}))


def generate_bad_req_response(message):
    return HttpResponseBadRequest(json.dumps({"status": "error", "message": message}))


def generate_resource_not_found_response(message):
    return Http404(json.dumps({"status": "error", "message": message}))


def generate_server_error_response(message):
    return HttpResponseServerError(json.dumps({"status": "error", "message": message}))


def validate_get_request(request):
    if "email" not in request.GET:
        return generate_bad_req_response("email not provided"), None
    return (None, request.GET["email"])


def validate_post_request(request):
    try:
        req_data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return generate_bad_req_response("invalid data"), None
    if "first_name" not in req_data or "email" not in req_data:
        return generate_bad_req_response("first_name/email not provided"), None
    return (None, req_data)


def validate_unsubscribe_request(request):
    try:
        req_data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return generate_bad_req_response("invalid data"), None
    if "email" not in req_data:
        return generate_bad_req_response("email not provided"), None
    return (None, req_data)


def index(request):
    if request.method == "GET":
        # validate request
        error, email = validate_get_request(request)
        # find user
        error, user_data = handle_finding_user(email)
        return generate_success_response(user_data)
    elif request.method == "POST":
        # validate request
        error, req_data = validate_post_request(request)
        if error:
            return error
        # add new user
        error = handle_adding_user(req_data)
        if error:
            return error
        return generate_success_response("added user")
    else:
        raise generate_resource_not_found_response("method not allowed")


def unsubscribe_user(request):
    if request.method == "POST":
        # validate request
        error, req_data = validate_unsubscribe_request(request)
        if error:
            return error
        # unsubscribe user
        error = handle_unsubscribing_user(req_data)
        if error:
            return error
        return generate_success_response("unsubscribed user")
    else:
        raise generate_resource_not_found_response("method not allowed")


def handle_finding_user(email):
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        raise generate_resource_not_found_response("user not found")
    except Exception:
        return generate_server_error_response("DB error")
    return None, {"first_name": user.first_name, "email": user.email, "active": user.active}


def handle_adding_user(req_data):
    first_name = req_data["first_name"]
    email = req_data["email"]
    # check if user with provided email exists
    if User.objects.filter(email=email):
        return generate_bad_req_response("user exists")
    # try to add user
    try:
        user = User(first_name=first_name, email=email)
        user.save()
    except Exception:
        return generate_server_error_response("DB error")


def handle_unsubscribing_user(req_data):
    email = req_data["email"]
    # check if user with provided email doesn't exists
    user = User.objects.filter(email=email)
    if not user:
        return generate_bad_req_response("invalid user")
    # try to update user with active=0
    try:
        user.update(active=0, updated_time=datetime.datetime.now(tz=timezone.utc))
    except Exception:
        return generate_server_error_response("DB error")

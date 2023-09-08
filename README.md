# EmailCampaignManager

## POST request to add a user

### Endpoint
```
curl --request POST --data '{"first_name": "gagan", "email": "narulagagandeepsingh@gmail.com"}' http://127.0.0.1:8000/usermanager
```

### Responses
```
> {"status": "success", "message": "added user"}
> {"status": "error", "message": "user exists"}
```

## GET request to fetch a user

## Endpoint
```
curl --request GET http://127.0.0.1:8000/usermanager?email=narulagagandeepsingh@gmail.com
```

## Responses
```
> {"status": "success", "message": {"first_name": "gagan", "email": "narulagagandeepsingh@gmail.com", "active": false}}
```

## POST request to unsubscribe user

### Endpoint
```
curl --request POST --data '{"email": "narulagagandeepsingh@gmail.com"}' http://127.0.0.1:8000/usermanager/unsubscribe
```

### Responses
```
> {"status": "success", "message": "unsubscribed user"}
> {"status": "error", "message": "invalid user"}
```

## POST request to send campaign emails to users

### Endpoint
```
curl --request POST http://127.0.0.1:8000/campaignmanager
```

### Responses
```
> {"status": "success"}
```

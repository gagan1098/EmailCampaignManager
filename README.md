
# POST request to add a user
```
curl --request POST --data '{"first_name": "gagan", "email": "narulagagandeepsingh@gmail.com"}' http://127.0.0.1:8000/usermanager
```

# GET request to fetch a user
```
curl --request GET http://127.0.0.1:8000/usermanager?email=narulagagandeepsingh@gmail.com
```

# POST request to unsubscribe user
```
curl --request POST --data '{"email": "narulagagandeepsingh@gmail.com"}' http://127.0.0.1:8000/usermanager/unsubscribe
```

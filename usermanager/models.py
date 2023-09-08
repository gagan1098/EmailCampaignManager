from datetime import datetime
from django.db import models


class User(models.Model):
    """
    User model
    """
    user_id = models.AutoField(primary_key=True)
    first_name = models.TextField(max_length=256, null=False)
    email = models.TextField(max_length=256, null=False)
    active = models.BooleanField(default=True, null=False)
    created_time = models.DateTimeField("created_time", default=datetime.now)
    updated_time = models.DateTimeField("updated_time", default=datetime.now)

    def __str__(self):
        return self.email

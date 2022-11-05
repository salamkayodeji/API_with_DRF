from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Event(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=200, default = "No Name")
    complete = models.BooleanField(default=False)
    date_created = models.DateField(auto_created=True)
    last_modified = models.DateField(auto_now=True)
    def __str__(self):
        return self.event_name

    


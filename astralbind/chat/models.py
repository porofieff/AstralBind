from django.db import models
from lk.models import UserProfile

class Pair_room(models.Model):
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name

class Message(models.Model):
    room = models.ForeignKey(Pair_room, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"{str(self.room)} - {str(self.sender)}"

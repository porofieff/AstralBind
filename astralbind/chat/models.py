from django.db import models
from lk.models import UserProfile
from django.utils import timezone

class Pair_room(models.Model):
    room_name = models.CharField(max_length=50, unique=True)
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1_rooms')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2_rooms')

    class Meta:
        unique_together = [['user1', 'user2']]

    def __str__(self):
        return self.room_name

class Message(models.Model):
    room = models.ForeignKey(Pair_room, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room}: {self.sender} -> {self.receiver} ({self.created_at})"
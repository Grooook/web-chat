from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'Chat: {self.name}'


class Participants(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)

    def __str__(self):
        return f'User: {self.user}, room: {self.room}'


class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    msg_text = models.CharField(max_length=255, verbose_name='Message text')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'In chat: {self.room} {self.user} write {self.msg_text} '


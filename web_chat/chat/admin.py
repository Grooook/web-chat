from django.contrib import admin
from .models import Room, Participants, Message

admin.site.register(Room)
admin.site.register(Participants)
admin.site.register(Message)

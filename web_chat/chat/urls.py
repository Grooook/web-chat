from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('home/', views.index,name='index'),
    path('chat/<room_name>/', views.room, name='room'),
    path('create_chat/', views.create_chat, name='create_chat'),
]

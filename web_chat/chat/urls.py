from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('home/', views.index,name='index'),
    path('chat/<room_id>/', views.room, name='room'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('delete_chat/<room_id>/', views.delete_chat, name='delete_chat'),
    path('add_to_room/<room_id>/', views.add_to_room, name='add_to_room'),

]

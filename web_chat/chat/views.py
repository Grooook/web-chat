from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Room,Participants,Message,User
from django.contrib.auth.decorators import login_required

def index(request):

    if request.user.is_authenticated:
        context = user_rooms(request)
        return render(request, 'base.html', context)

    context = {
        'rooms':[]
    }
    return render(request, 'base.html',context)

def room(request, room_name):

    context = {
        'room_name': room_name
    }
    return render(request, 'chat/room.html', context)

@login_required(login_url='/login/')
def create_chat(request):
    
    if request.POST:
        user = User.objects.get(username = request.user)
        all_user_rooms = user_rooms(request)
        room_name = request.POST.get('room_name')

        if not is_room_exist(room_name, all_user_rooms['rooms']):
            room = Room(name=room_name,owner=user)
            room.save()
            Participants(user=user,room=room).save()

            return redirect('/home/')
        else:
            messages.info(request, 'You already have a chat with this name')

    context =  user_rooms(request)
    
    return render(request, 'chat/create_room.html', context)

def is_room_exist(room_name, room_list):
    for room in room_list:
        if room_name == room.name:
            return True

    return False

def user_rooms(request):
    participants = Participants.objects.filter(user=request.user)
    rooms = []
    for i in participants:
        rooms.append(Room.objects.get(id=i.room.id))
    
    context = {
        'rooms' : rooms
    }

    return context
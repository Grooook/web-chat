from django.contrib import messages
from django.shortcuts import get_object_or_404 , render, redirect
from .models import Room, Participants, Message, User
from django.contrib.auth.decorators import login_required
from channels.db import database_sync_to_async

def index(request):

    if request.user.is_authenticated:
        context = user_rooms(request)
        return render(request, 'base.html', context)

    context = {
        'rooms': []
    }
    return render(request, 'base.html', context)


@login_required(login_url='/login/')
def room(request, room_id):

    if get_object_or_none(Participants, room=room_id, user=request.user) is None:
        return redirect ('/login/')

    room_messages = Message.objects.filter(room=room_id)
    
    context = {
        'room_id': room_id,
        'user_name': request.user.username,
        'room_messages' : room_messages,
    }

    context |= user_rooms(request)
    return render(request, 'chat/room.html', context)


@login_required(login_url='/login/')
def create_chat(request):

    if request.POST:
        user = User.objects.get(username=request.user)
        all_user_rooms = user_rooms(request)
        room_name = request.POST.get('room_name')

        if not is_room_exist(room_name, all_user_rooms['rooms']):
            room = Room(name=room_name, owner=user)
            room.save()
            Participants(user=user, room=room).save()

            return redirect('/home/')
        else:
            messages.info(request, 'You already have a chat with this name')

    context = user_rooms(request)

    return render(request, 'chat/create_room.html', context)

@login_required(login_url='/login/')
def delete_chat(request, room_id):
    
    Participants.objects.filter(room = room_id, user = request.user).delete()

    return redirect('/home/')

def is_room_exist(room_name, room_list):
    for room in room_list:
        if room_name == room.name:
            return True

    return False

def add_to_room(request,room_id):
    
    if request.POST:
        username = request.POST.get('username')
        user = get_object_or_none(User,username=username)
        print(user)
        if user is not None:
            room = Room.objects.get(pk=room_id)

            if get_object_or_none(Participants,user=user,room=room) is None:
                Participants(user=user,room=room).save()

                return redirect (f'/chat/{room_id}/')
            else:
                messages.info(request,'This user is already in the room')
        else:
            messages.info(request,'No such user exists')

    context = {
        'room_id' : room_id,
    }
    context |= user_rooms(request)

    return render(request, 'chat/add_user.html', context)

def user_rooms(request):
    participants = Participants.objects.filter(user=request.user)
    rooms = []
    for i in participants:
        rooms.append(Room.objects.get(id=i.room.id))

    context = {
        'rooms': rooms
    }

    return context

def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj 

@database_sync_to_async
def leave_message(user_name, room_name, message):
    user = User.objects.get(username=user_name)
    room = Room.objects.get(id=room_name)
    Message(user=user, room=room, msg_text=message).save()

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Pair_room, Message
from lk.models import UserProfile


@login_required
def chat_view(request, match_id):
    existing_room = Pair_room.objects.get(room_name__icontains=match_id)
    get_messages = Message.objects.filter(room=existing_room)


    context = {
        "messages": get_messages,
        "user": request.user.username,
        "room_name": existing_room.room_name,
    }
    return render(request, 'chat.html', context)

def chat_room(request, room_name):
    room = get_object_or_404(Pair_room, room_name=room_name)

    messages = Message.objects.filter(room=room)

    context = {
        "room_name": room_name,
        "messages": messages,
        "user": request.user.username
    }
    return render(request, 'chat/chat.html', context)

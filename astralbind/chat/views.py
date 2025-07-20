from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Pair_room, Message
from lk.models import UserProfile, Favorite
from chat_room import *

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


@login_required
def chat_room(request, room_name):
    room = get_object_or_404(Pair_room, room_name=room_name)

    if request.user not in [room.user1.user, room.user2.user]:
        return HttpResponseForbidden("Доступ запрещен")

    messages = Message.objects.filter(room=room).order_by('created_at')
    interlocutor = room.user1 if request.user == room.user2.user else room.user2

    is_favorite = Favorite.objects.filter(
        user=request.user.userprofile,
        favorite_user=interlocutor
    ).exists()

    context = {
        'room': room,
        'room_name': room_name,
        'messages': messages,
        'interlocutor': interlocutor,
        'user': request.user,
        'is_favorite': is_favorite,
        'current_user': request.user,
    }
    return render(request, 'chat/chat.html', context)


@login_required
@require_POST
def toggle_favorite(request, user_id):
    target_user = get_object_or_404(UserProfile, user__id=user_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user.userprofile,
        favorite_user=target_user
    )
    if not created:
        favorite.delete()
    return redirect('chat-room', room_name=request.POST.get('room_name'))

def user_profile_redirect(request, user_id):
    return redirect('user_profile', user_id=user_id)

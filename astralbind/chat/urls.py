from django.urls import path
from chat import views

urlpatterns = [
    path('chat/<str:room_name>/', views.chat_room, name='chat-room'),
    path('user/<int:user_id>/', views.user_profile_redirect, name='user_profile_redirect'),
]

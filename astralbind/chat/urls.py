from django.urls import path
from .views import chat_view

urlpatterns = [
    path("<str:match_id>/", chat_view, name='chat')
]

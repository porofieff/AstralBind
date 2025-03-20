from django.urls import path
from lk.views import index

urlpatterns = [
    path('lk/', index),
]

from django.urls import path
from . import views

urlpatterns = [
    path('author/auth', views.Reg),
    path('author/afroris', views.Avtoris)
]

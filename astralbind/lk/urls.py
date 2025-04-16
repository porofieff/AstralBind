from django.urls import path, include
from . import views
from chat import urls

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.index, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('main_page/', views.main_page, name='main_page'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('my_chats/', views.chat_list, name='chats_list'),
    path('chat/', include('chat.urls')),
    path('select_ahp', views.select_ahp, name='select_ahp'),
]

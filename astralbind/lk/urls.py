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
    path('select_ahp/', views.select_ahp, name='select_ahp'),
    path('main_ahp/', views.main_ahp, name='main_ahp'),
    path('filter_ahp/', views.filter_ahp, name='filter_ahp'),
    path('evaluate_user/', views.evaluate_user, name='evaluate_user'),
    path('next_user/', views.next_user, name='next_user'),
    path('results/', views.results, name='results'),
    path('start_chat/<int:user_id>/', views.start_chat, name='start_chat'),
    path('favorite/toggle/<int:user_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path('add_comment/<int:user_id>/', views.add_comment, name='add_comment'),
    path('clear-session/', views.clear_session, name='clear_session'),
]

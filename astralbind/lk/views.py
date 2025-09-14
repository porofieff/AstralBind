from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Exists, OuterRef
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, CommentForm
from .forms import UserProfileForm
from .models import UserProfile, Hobby, ZodiacSign, Education, HobbyGroup, UserFilters, City, Favorite, Comment
from chat.models import Pair_room, Message
import random
import numpy as np
import statistics as stat
from django.urls import reverse
from ahp_mothods import *
import json


def index(request):
    return render(request, 'index.html')

@login_required
def main_page(request):
    return render(request, 'main_page.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'registration.html', {'form': form})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return render(request, 'registration.html', {'form': form})

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
        else:
            messages.error(request, 'Ошибка регистрации! Попробуйте снова.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'login.html')


weight_criter = []
@login_required
def profile_edit(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    zodiac_signs = ZodiacSign.objects.all()
    educations = Education.objects.all()

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()
        user_profile.education_id = request.POST.get('education')
        user_profile.zodiac_sign_id = request.POST.get('zodiac_sign')
        user_profile.city = request.POST.get('city')
        user_profile.children_count = request.POST.get('children_count')
        user_profile.hobby_description = request.POST.get('hobby_description')
        user_profile.life_goal = request.POST.get('life_goal')
        user_profile.character = request.POST.get('character')
        user_profile.sex = request.POST.get('sex')
        user_profile.age = request.POST.get('age')

        user_profile.hide_age = request.POST.get('hide_age') == 'True'
        user_profile.hide_city = request.POST.get('hide_city') == 'True'
        user_profile.hide_zodiac = request.POST.get('hide_zodiac') == 'True'
        user_profile.hide_education = request.POST.get('hide_education') == 'True'
        user_profile.hide_hobbies = request.POST.get('hide_hobbies') == 'True'
        user_profile.hide_hobby_description = request.POST.get('hide_hobby_description') == 'True'
        user_profile.hide_life_goal = request.POST.get('hide_life_goal') == 'True'
        user_profile.hide_character = request.POST.get('hide_character') == 'True'
        user_profile.hide_children = request.POST.get('hide_children') == 'True'

        hobbies = request.POST.getlist('hobbies')
        user_profile.hobbies.set(Hobby.objects.filter(id__in=hobbies))

        user_profile.city_vs_hobby = request.POST.get('city_vs_hobby')
        user_profile.city_vs_zodiac = request.POST.get('city_vs_zodiac')
        user_profile.city_vs_education = request.POST.get('city_vs_education')
        user_profile.education_vs_hobby = request.POST.get('education_vs_hobby')
        user_profile.education_vs_zodiac = request.POST.get('education_vs_zodiac')
        user_profile.hobby_vs_zodiac = request.POST.get('hobby_vs_zodiac')

        self_city_vs_hobby = float(translate[request.POST.get('city_vs_hobby')])
        self_city_vs_zodiac = float(translate[request.POST.get('city_vs_zodiac')])
        self_city_vs_education = float(translate[request.POST.get('city_vs_education')])
        self_education_vs_hobby = float(translate[request.POST.get('education_vs_hobby')])
        self_education_vs_zodiac = float(translate[request.POST.get('education_vs_zodiac')])
        self_hobby_vs_zodiac = float(translate[request.POST.get('hobby_vs_zodiac')])

        self_matrix = matrix_filling(self_city_vs_hobby, self_city_vs_zodiac, self_city_vs_education,
            self_education_vs_hobby, self_education_vs_zodiac, self_hobby_vs_zodiac)

        weight_criter = get_weight_critier(self_matrix)

        json_weight_criter = json.dumps(weight_criter)
        user_profile.weights_for_ahp = json_weight_criter

        user_profile.user_CR = get_user_CR(self_matrix)

        if 'photo' in request.FILES:
            uploaded_file = request.FILES['photo']
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, "Файл слишком большой (максимум 5MB)")
                return redirect('profile_edit')
            user_profile.photo = uploaded_file

        user_profile.save()
        return redirect('profile')
    else:
        zodiac_signs = ZodiacSign.objects.all()
        hobby_groups = HobbyGroup.objects.prefetch_related('hobby_set').all()
        return render(request, 'profile_edit.html', {'user_profile': user_profile, 'hobby_groups': hobby_groups,
            'zodiac_signs': zodiac_signs, 'educations': educations})

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    criteria_names = ['Город', 'Хобби', 'Знак зодиака', 'Образование']
    weights = []

    if user_profile.weights_for_ahp:
        try:
            weights = json.loads(user_profile.weights_for_ahp)
        except json.JSONDecodeError:
            weights = []

    weights_with_names = list(zip(criteria_names, weights))
    comments = Comment.objects.filter(target_user=user_profile).select_related('author__user').order_by('-created_at')

    return render(request, 'profile_view.html', {
        'profile_view': user_profile,
        'weights_with_names': weights_with_names,
        'comments': comments
    })

@login_required
def start_chat(request, user_id):
    current_user = request.user.userprofile
    target_user = get_object_or_404(UserProfile, user__id=user_id)

    room = Pair_room.objects.filter((Q(user1=current_user) & Q(user2=target_user)) | (Q(user1=target_user) & Q(user2=current_user))).first()

    if not room:
        room_name = f"chat_{current_user.id}_{target_user.id}"
        room = Pair_room.objects.create(
            room_name=room_name,
            user1=current_user,
            user2=target_user
        )
        Message.objects.create(
            room=room,
            sender=current_user,
            receiver=target_user,
            message="Чат начат!"
        )

    return redirect('chat-room', room_name=room.room_name)

@login_required
def main_ahp(request):
    return render(request, 'main_ahp.html')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')

@login_required
def chat_list(request):
    user_profile = request.user.userprofile
    user_rooms = Pair_room.objects.filter(Q(user1=user_profile) | Q(user2=user_profile)).distinct()

    return render(request, 'chat_list.html', {'chats': user_rooms})


@login_required
def filter_ahp(request):
    user_filters, created = UserFilters.objects.get_or_create(user=request.user)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    zodiac_signs = ZodiacSign.objects.all()
    cities = City.objects.all()
    hobbies = Hobby.objects.all()
    educations = Education.objects.all()

    if request.method == 'POST':
        user = request.user
        user_filters.education_id = request.POST.get('education')
        user_filters.zodiac_sign_id = request.POST.get('zodiac_sign')
        user_filters.city = request.POST.get('city')
        if request.POST.get('city') == '':
            user_filters.city =  user_profile.city

        hobbies = request.POST.getlist('hobbies')
        user_filters.hobbies.set(Hobby.objects.filter(id__in=hobbies))
        user_filters.save()
        return redirect('main_ahp')
    else:
        zodiac_signs = ZodiacSign.objects.all()
        hobby_groups = HobbyGroup.objects.prefetch_related('hobby_set').all()
        return render(request, 'filter_ahp.html',
                      {'user_filters': user_filters, 'hobby_groups': hobby_groups, 'zodiac_signs': zodiac_signs, 'cities': cities,
                       'educations': educations})

@login_required
def evaluate_user(request):
    if 'new_search' in request.GET:
        request.session['shown_users'] = []
        request.session['ratings'] = []
        request.session['current_user_id'] = None
        request.session.modified = True

    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('profile_edit')


    if not user_profile.sex or not request.user.first_name or not request.user.last_name:
        return redirect('profile_edit')
    favorite_users = Favorite.objects.filter(user=user_profile).values_list('favorite_user_id', flat=True)


    try:
        current_user_sex = request.user.userprofile.sex
    except UserProfile.DoesNotExist:
        return redirect('profile_edit')
    users = UserProfile.objects.exclude(user=request.user)

    opposite_sex = 2 if current_user_sex == 1 else 1

    users = UserProfile.objects.exclude(
        Q(user=request.user) |
        Q(id__in=favorite_users)
    ).filter(sex=opposite_sex)

    try:
        user_filters = UserFilters.objects.get(user=request.user)

        if user_filters.city:
            users = users.filter(city=user_filters.city)
        if user_filters.zodiac_sign:
            users = users.filter(zodiac_sign=user_filters.zodiac_sign)
        if user_filters.education:
            users = users.filter(education=user_filters.education)
        if user_filters.hobbies.exists():
            query = Q()
            for hobby in user_filters.hobbies.all():
                query |= Q(hobbies=hobby)
            users = users.filter(query).distinct()
    except UserFilters.DoesNotExist:
        pass

    shown_users = request.session.get('shown_users', [])
    available_users = users.exclude(id__in=shown_users)

    if request.method == 'POST':
        current_user_id = request.session.get('current_user_id')
        if current_user_id:
            ratings = request.session.get('ratings', [])
            ratings.append({
                'user_id': current_user_id,
                'hobby_rating': request.POST.get('hobby_rating', 5),
                'city_rating': request.POST.get('city_rating', 5),
                'zodiac_rating': request.POST.get('zodiac_rating', 5),
                'education_rating': request.POST.get('education_rating', 5)
            })
            request.session['ratings'] = ratings
            request.session.modified = True

            if len(ratings) >= 5:
                return redirect('results')

    if not available_users.exists() and len(shown_users) >= 1:
        return redirect('results')

    if not available_users.exists() and not shown_users:
        return render(
            request,
            'no_users_found.html',
            {'redirect_url': reverse('filter_ahp')},
            status=404
        )
    try:
        random_user = random.choice(available_users)
    except IndexError:
        return redirect('results')

    shown_users.append(random_user.id)
    request.session['shown_users'] = shown_users
    request.session['current_user_id'] = random_user.id
    request.session.modified = True

    is_final = len(shown_users) >= 5 or len(available_users) == 1

    return render(request, 'evaluate_user.html', {
        'user_profile': random_user,
        'is_final': is_final
    })

@login_required
def results(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    ratings = request.session.get('ratings', [])
    user_ids = [r['user_id'] for r in ratings]
    users = UserProfile.objects.filter(id__in=user_ids)
    cnt_users = len(ratings)

    if cnt_users == 0:
        return render(request, 'results.html', {'result_data': []})

    matrix_hobby = np.ones((cnt_users, cnt_users))
    matrix_zodiac = np.ones((cnt_users, cnt_users))
    matrix_education = np.ones((cnt_users, cnt_users))
    matrix_city = np.ones((cnt_users, cnt_users))

    for i, rating in enumerate(ratings):
        user_hobby_rating = str(rating['hobby_rating'])
        user_city_rating = str(rating['city_rating'])
        user_zodiac_rating = str(rating['zodiac_rating'])
        user_education_rating = str(rating['education_rating'])

        for j in range(i + 1, cnt_users):
            matrix_hobby[i][j] = translate[user_hobby_rating]
            matrix_hobby[j][i] = 1 / translate[user_hobby_rating]
            matrix_city[i][j] = translate[user_city_rating]
            matrix_city[j][i] = 1 / translate[user_city_rating]
            matrix_zodiac[i][j] = translate[user_zodiac_rating]
            matrix_zodiac[j][i] = 1 / translate[user_zodiac_rating]
            matrix_education[i][j] = translate[user_education_rating]
            matrix_education[j][i] = 1 / translate[user_education_rating]

    norm_hobbies = norm_calculate(matrix_hobby)
    norm_zodiac = norm_calculate(matrix_zodiac)
    norm_education = norm_calculate(matrix_education)
    norm_city = norm_calculate(matrix_city)

    norm_all_matrix = np.array([norm_hobbies, norm_zodiac, norm_education, norm_city])

    user_weights = json.loads(user_profile.weights_for_ahp)
    result = np.dot(user_weights, norm_all_matrix)

    result_data = []
    for i, rating in enumerate(ratings):
        try:
            user = users.get(id=rating['user_id'])
            compatibility_percent = round(result[i] * 100, 1)

            is_favorite = Favorite.objects.filter(
                user=user_profile,
                favorite_user=user
            ).exists()

            result_data.append({
                'user': user,
                'rating': rating,
                'compatibility': compatibility_percent,
                'is_favorite': is_favorite,
            })
        except UserProfile.DoesNotExist:
            continue

    result_data.sort(key=lambda x: x['compatibility'], reverse=True)

    response = render(request, 'results.html', {'result_data': result_data})
    request.session.modified = True
    return response


@login_required
@require_POST
def toggle_favorite(request, user_id):
    try:
        user_profile = request.user.userprofile
        target_user = get_object_or_404(UserProfile, user__id=user_id)
        favorite = Favorite.objects.filter(user=user_profile, favorite_user=target_user).first()
        if favorite:
            favorite.delete()
        else:
            Favorite.objects.create(user=user_profile, favorite_user=target_user)

        redirect_to = request.POST.get('redirect_to', '')

        if redirect_to == 'chat':
            room_name = request.POST.get('room_name', '')
            if room_name:
                return redirect('chat-room', room_name=room_name)
            return redirect('chats_list')

        elif redirect_to == 'results':
            return redirect('results')
        elif redirect_to == 'favorites':
            return redirect('favorite_list')
        else:
            return redirect('main_page')

    except Exception as e:
        return redirect('main_page')


@login_required
def favorite_list(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('profile_edit')

    favorites = Favorite.objects.filter(user=user_profile).select_related('favorite_user')
    favorites_data = []

    for favorite in favorites:
        target_user = favorite.favorite_user
        is_mutual = Favorite.objects.filter(
            user=target_user,
            favorite_user=user_profile
        ).exists()
        room = Pair_room.objects.filter(
            Q(user1=user_profile, user2=target_user) |
            Q(user1=target_user, user2=user_profile)
        ).first()

        message_count = Message.objects.filter(room=room).count() if room else 0

        favorites_data.append({
            'favorite': favorite,
            'is_mutual': is_mutual,
            'message_count': message_count
        })

    return render(request, 'favorites.html', {'favorites_data': favorites_data})

@login_required
def clear_session(request):
    if request.method == 'POST':
        request.session.pop('ratings', None)
        request.session.pop('shown_users', None)
    return redirect('main_ahp')

def next_user(request):
    return evaluate_user(request)


@login_required
def add_comment(request, user_id):
    target_user = get_object_or_404(UserProfile, user__id=user_id)
    author_profile = request.user.userprofile

    is_mutual = Favorite.objects.filter(
        user=target_user,
        favorite_user=author_profile
    ).exists()

    room = Pair_room.objects.filter(
        (Q(user1=author_profile) & Q(user2=target_user)) |
        (Q(user1=target_user) & Q(user2=author_profile))
    ).first()
    message_count = Message.objects.filter(room=room).count() if room else 0

    if not is_mutual or message_count <= 10:
        return HttpResponseForbidden("У вас нет прав оставлять комментарии этому пользователю")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = author_profile
            comment.target_user = target_user
            comment.save()
            return redirect('user_profile', user_id=user_id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {
        'form': form,
        'target_user': target_user
    })


@login_required
def user_profile(request, user_id):
    target_user = get_object_or_404(UserProfile, user__id=user_id)
    comments = Comment.objects.filter(target_user=target_user).select_related('author__user')
    return render(request, 'user_profile.html', {
        'target_user': target_user,
        'comments': comments
    })

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm
from .forms import UserProfileForm
from .models import UserProfile, Hobby, ZodiacSign, Education, HobbyGroup, UserFilters, City
from chat.models import Pair_room, Message
import random
import numpy as np
import statistics as stat
from django.urls import reverse
import json

translate = {
    '1': 0.2,
    '2': 0.3,
    '3': 1.0,
    '4': 3.0,
    '5': 5.0
}

RI = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
}

def norm_calculate(matrix):
    weight_criter = []
    arr_avg_geom = []
    for i in matrix:
        elem_matrix = [float(j) for j in i]
        avg_geom = stat.geometric_mean(elem_matrix)
        arr_avg_geom.append(avg_geom)
    for i in range(len(arr_avg_geom)):
        value = arr_avg_geom[i] / sum(arr_avg_geom)
        weight_criter.append(value)
    return weight_criter

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
            messages.success(request, 'Вы успешно зарегистрированы!')
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

        hobbies = request.POST.getlist('hobbies')
        user_profile.hobbies.set(Hobby.objects.filter(id__in=hobbies))

        user_profile.city_vs_hobby = request.POST.get('city_vs_hobby')
        user_profile.city_vs_zodiac = request.POST.get('city_vs_zodiac')
        user_profile.city_vs_education = request.POST.get('city_vs_education')
        user_profile.education_vs_hobby = request.POST.get('education_vs_hobby')
        user_profile.education_vs_zodiac = request.POST.get('education_vs_zodiac')
        user_profile.hobby_vs_zodiac = request.POST.get('hobby_vs_zodiac')

        self_city_vs_hobby = translate[request.POST.get('city_vs_hobby')]
        self_city_vs_zodiac = translate[request.POST.get('city_vs_zodiac')]
        self_city_vs_education = translate[request.POST.get('city_vs_education')]
        self_education_vs_hobby = translate[request.POST.get('education_vs_hobby')]
        self_education_vs_zodiac = translate[request.POST.get('education_vs_zodiac')]
        self_hobby_vs_zodiac = translate[request.POST.get('hobby_vs_zodiac')]

        self_matrix = np.ones((4, 4), dtype=float)
        self_matrix[0][1] = self_city_vs_hobby
        self_matrix[1][0] = 1 / self_city_vs_hobby
        self_matrix[0][2] = self_city_vs_zodiac
        self_matrix[2][0] = 1 / self_city_vs_zodiac
        self_matrix[0][3] = self_city_vs_education
        self_matrix[3][0] = 1 / self_city_vs_education
        self_matrix[1][3] = 1 / self_education_vs_hobby
        self_matrix[3][1] = self_education_vs_hobby
        self_matrix[2][3] = 1 / self_education_vs_zodiac
        self_matrix[3][2] = self_education_vs_zodiac
        self_matrix[1][2] = self_hobby_vs_zodiac
        self_matrix[2][1] = 1 / self_hobby_vs_zodiac

        weight_criter = []
        arr_avg_geom = []
        for i in self_matrix:
            elem_self_matrix = [float(j) for j in i]
            avg_geom = stat.geometric_mean(elem_self_matrix)
            arr_avg_geom.append(avg_geom)
        for i in range(len(arr_avg_geom)):
            value = arr_avg_geom[i] / sum(arr_avg_geom)
            weight_criter.append(value)

        json_weight_criter = json.dumps(weight_criter)
        user_profile.weights_for_ahp = json_weight_criter

        w = self_matrix.sum(axis=0)
        normalized_self_matrix = self_matrix / w
        w = normalized_self_matrix.mean(axis=1)
        self_matrixw = self_matrix.dot(w)
        lambda_max = np.mean(self_matrixw / w)
        n = self_matrix.shape[0]
        CI = (lambda_max - n) / (n - 1)

        CR = CI / RI.get(len(self_matrix)) * 100
        user_profile.user_CR = CR

        if 'photo' in request.FILES:
            uploaded_file = request.FILES['photo']
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, "Файл слишком большой (максимум 5MB)")
                return redirect('profile_edit')
            user_profile.photo = uploaded_file

        user_profile.save()
        messages.success(request, 'Данные успешно обновлены!')
        return redirect('profile')
    else:
        zodiac_signs = ZodiacSign.objects.all()
        hobby_groups = HobbyGroup.objects.prefetch_related('hobby_set').all()
        return render(request, 'profile_edit.html', {'user_profile': user_profile, 'hobby_groups': hobby_groups, 'zodiac_signs': zodiac_signs, 'educations': educations})

@login_required
def profile_view(request):
    return render(request, 'profile_view.html')

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
def select_ahp(request):
    return render(request, 'select_ahp.html')

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
def view_form(request):
    return render(request, 'evaluate_user.html')

from django.db.models import Q

@login_required
def evaluate_user(request):
    if 'new_search' in request.GET:
        request.session['shown_users'] = []
        request.session['ratings'] = []
        request.session['current_user_id'] = None
        request.session.modified = True

    try:
        user_filters = UserFilters.objects.get(user=request.user)
    except UserFilters.DoesNotExist:
        user_filters = None

    users = UserProfile.objects.exclude(user=request.user)

    if user_filters:
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

    shown_users = request.session.get('shown_users', [])
    available_users = users.exclude(id__in=shown_users)

    if not available_users.exists() and not shown_users:
        return render(
            request,
            'no_users_found.html',
            {'redirect_url': reverse('filter_ahp')},
            status=404
        )

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

    try:
        random_user = random.choice(available_users)
    except IndexError:
        return redirect('results')

    shown_users.append(random_user.id)
    request.session['shown_users'] = shown_users
    request.session['current_user_id'] = random_user.id
    request.session.modified = True
    is_final = len(shown_users) >= 5 or len(shown_users) >= available_users.count()

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
        user_hobby_rating = int(rating['hobby_rating'])
        user_city_rating = int(rating['city_rating'])
        user_zodiac_rating = int(rating['zodiac_rating'])
        user_education_rating = int(rating['education_rating'])

        for j in range(i + 1, cnt_users):
            matrix_hobby[i][j] = user_hobby_rating
            matrix_hobby[j][i] = 1 / user_hobby_rating
            matrix_city[i][j] = user_city_rating
            matrix_city[j][i] = 1 / user_city_rating
            matrix_zodiac[i][j] = user_zodiac_rating
            matrix_zodiac[j][i] = 1 / user_zodiac_rating
            matrix_education[i][j] = user_education_rating
            matrix_education[j][i] = 1 / user_education_rating

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
            result_data.append({
                'user': user,
                'rating': rating,
                'compatibility': compatibility_percent
            })
        except UserProfile.DoesNotExist:
            continue

    result_data.sort(key=lambda x: x['compatibility'], reverse=True)

    response = render(request, 'results.html', {'result_data': result_data})
    request.session['shown_users'] = []
    request.session['ratings'] = []
    request.session.modified = True
    return response
def next_user(request):
    return evaluate_user(request)

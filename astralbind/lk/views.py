from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .forms import UserProfileForm
from .models import UserProfile, Hobby



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
@login_required
def profile_edit(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()

        user_profile.children_count = request.POST.get('children_count')
        user_profile.hobby_description = request.POST.get('hobby_description')
        user_profile.life_goal = request.POST.get('life_goal')
        user_profile.character = request.POST.get('character')

        hobbies = request.POST.getlist('hobbies')
        user_profile.hobbies.set(Hobby.objects.filter(id__in=hobbies))

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
        hobbies = Hobby.objects.all()
        return render(request, 'profile_edit.html', {'user_profile': user_profile, 'hobbies': hobbies})

@login_required
def profile_view(request):
    return render(request, 'profile_view.html')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')
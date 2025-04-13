from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Hobby


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        min_length=4,
        max_length=20,
        widget=forms.TextInput(attrs={
            'pattern': '[A-Za-z0-9_]{4,20}',
            'title': 'Логин должен содержать от 4 до 20 символов (латинские буквы, цифры и подчеркивание)'
        })
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'pattern': '^(?=.*[A-Za-z])(?=.*\d).{8,}$',
            'title': 'Пароль должен содержать минимум 8 символов, включая буквы и цифры'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    hobbies = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = UserProfile
        fields = ['photo', 'hobbies', 'children_count', 'hobby_description', 'life_goal', 'character']

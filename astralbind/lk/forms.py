from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Hobby

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    hobbies = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = UserProfile
        fields = ['photo', 'hobbies', 'children_count', 'hobby_description', 'life_goal', 'character']

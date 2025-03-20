#from django.http.request import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Страница, где когда-нибудь будет личный кабинет :)))))")

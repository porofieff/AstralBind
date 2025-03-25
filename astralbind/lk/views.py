from django.shortcuts import render
from django.db import connection


def Reg(request):
    return render(request, "Reg.html")

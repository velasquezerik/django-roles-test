from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# Create your views here.


def index(request):
	return render(request, 'website/index.html', {})


def login(request):
	return render(request,'website/login.html',{})
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from rolepermissions.shortcuts import assign_role
from rolepermissions.verifications import has_permission
from roles import SystemAdmin, SystemUser

def guest(user):
    return not user.is_authenticated()

# Create your views here.


def index(request):
	return render(request, 'website/index.html', {})


def login(request):
	if not request.user.is_authenticated():
		user = User.objects.get(id=2)
		assign_role(user, SystemAdmin)
		print user
		return render(request,'website/login.html',{})
	else:
		return redirect("/")


@login_required(login_url="/login/")
def logout_user(request):
	logout(request)
	return redirect("/login/")






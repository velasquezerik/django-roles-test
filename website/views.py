from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required,user_passes_test
from rolepermissions.shortcuts import assign_role, remove_role
from rolepermissions.verifications import has_permission, has_role
from rolepermissions.decorators import has_role_decorator
from roles import SystemAdmin, SystemUser

# Create your views here.


def index(request):
	return render(request, 'website/index.html', {})



		#user = User.objects.get(id=3)
		#assign_role(user, "system_admin")
		#if has_role(user, ['system_admin']):
		#	print 'User is a Admin'
		#else:
		#	print "User is a simple user"

#login users
def login_user(request):
	if not request.user.is_authenticated():
		if request.method == "POST":
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					if has_role(user, ['system_admin']):
						return redirect("/admin/")
					else:
						return redirect("/user/")
				else:
					return render(request, 'website/login.html', {'error_message': 'Your account has been disabled'})
			else:
				return render(request, 'website/login.html', {'error_message': 'Invalid username or password'})
		return render(request,'website/login.html',{})
	else:
		return redirect("/")


@login_required(login_url="/login/")
def logout_user(request):
	logout(request)
	return redirect("/login/")


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def test(request):

	user = User.objects.get(id=1)
	remove_role(user)
	assign_role(user, "system_admin")
	print "Funcionooooooooo"
	if has_role(user, ['system_admin']):
		print 'User is a Admin'
	if has_role(user, ['system_user']):
		print 'User is a User'
	return redirect("/")


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_view(request):
	return render(request,'admin/index.html',{})

@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_view(request):
	return render(request,'user/index.html',{})


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_profile(request):
	user = User.objects.get(id = request.user.id)
	return render(request,'admin/profile.html',{'user':user})

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_profile_update(request):
	if request.method == "POST":
		user = User.objects.get(id=request.user.id)
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email= request.POST['email']

		#update user
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.save()
	
	return redirect("/admin/profile/")







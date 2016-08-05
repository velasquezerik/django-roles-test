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
from models import UserImage

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

		#update image to user
		if 'image' in request.FILES:
			image = UserImage.objects.get(user_id = user.id)
			image.model_pic = request.FILES['image']
			image.user = user
			image.save()

		try:
			user = User.objects.get(email=email)
		except Exception, e:
			pass
		else:
			if user.email == email:
				pass
			else:
				return redirect("/admin/profile/")


		#update user
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.save()
	
	return redirect("/admin/profile/")


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_show_users(request):
	users = User.objects.all()
	return render(request,'admin/users_list.html',{'users':users})

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_create_user(request):
	users = User.objects.all()
	if request.method == "POST":
		#create a new user
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email= request.POST['email']
		username = request.POST['username']

		try:
			user = User.objects.get(username=username)
		except Exception, e:
			pass
		else:
			return render(request,'admin/users_create.html',{'users':users,'error_message':'Invalid Username'})

		try:
			user = User.objects.get(email=email)
		except Exception, e:
			pass
		else:
			return render(request,'admin/users_create.html',{'users':users,'error_message':'Invalid Email'})

		user = User()
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.username = username
		user.set_password('1q2w3e4r5t')
		user.is_active = True
		user.save()

		#create role for user
		assign_role(user, "system_user")

		#create image for user
		image = UserImage()
		image.user = user
		image.save()

		#send email to user

		#return to list users
		return redirect("/admin/users/")

	return render(request,'admin/users_create.html',{'users':users})


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_show(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except Exception, e:
		return redirect("/admin/users/")
	
	return render(request,'admin/show_user.html',{'user_show':user})


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_delete(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except Exception, e:
		return redirect("/admin/users/")

	user.is_active = False
	user.save()
	return redirect("/admin/users/")


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_active(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except Exception, e:
		return redirect("/admin/users/")

	user.is_active = True
	user.save()
	return redirect("/admin/users/")



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_create_admin(request):
	users = User.objects.all()
	if request.method == "POST":
		#create a new user
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email= request.POST['email']
		username = request.POST['username']

		try:
			user = User.objects.get(username=username)
		except Exception, e:
			pass
		else:
			return render(request,'admin/admins_create.html',{'users':users,'error_message':'Invalid Username'})

		try:
			user = User.objects.get(email=email)
		except Exception, e:
			pass
		else:
			return render(request,'admin/admins_create.html',{'users':users,'error_message':'Invalid Email'})

		user = User()
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.username = username
		user.set_password('1q2w3e4r5t')
		user.is_active = True
		user.is_superuser = True
		user.is_staff= True
		user.save()

		#create role for user
		assign_role(user, "system_admin")

		#create image for user
		image = UserImage()
		image.user = user
		image.save()

		#send email to user


		#return to list users
		return redirect("/admin/users/")

	return render(request,'admin/admins_create.html',{'users':users})




@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_edit(request, user_id):
	try:
		user = User.objects.get(id=user_id)
	except Exception, e:
		return redirect("/admin/users/")
	
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email= request.POST['email']

		try:
			user = User.objects.get(email=email)
		except Exception, e:
			pass
		else:
			if user.email == email:
				pass
			else:
				return render(request,'admin/edit_user.html',{'user_show':user,'error_message':'Invalid Email'})


		#update user
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.save()

		return redirect("/admin/users/")

	return render(request,'admin/edit_user.html',{'user_show':user})


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_password(request):

	user = User.objects.get(id=request.user.id)

	if request.method == 'POST':
		new_password = request.POST['new_password']
		rep_password = request.POST['repeat_password']

		if new_password == rep_password:
			#update password
			user.set_password(new_password)
			user.save()
			logout(request)
			return redirect("/login/")

	return redirect("/admin/profile/")




@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_profile(request):
	user = User.objects.get(id = request.user.id)
	return render(request,'user/profile.html',{'user':user})


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_profile_update(request):
	if request.method == "POST":
		user = User.objects.get(id=request.user.id)
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email= request.POST['email']

		#update image to user
		if 'image' in request.FILES:
			image = UserImage.objects.get(user_id = user.id)
			image.model_pic = request.FILES['image']
			image.user = user
			image.save()

		try:
			user = User.objects.get(email=email)
		except Exception, e:
			pass
		else:
			if user.email == email:
				pass
			else:
				return redirect("/user/profile/")


		#update user
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.save()
	
	return redirect("/user/profile/")


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_password(request):

	user = User.objects.get(id=request.user.id)

	if request.method == 'POST':
		new_password = request.POST['new_password']
		rep_password = request.POST['repeat_password']

		if new_password == rep_password:
			#update password
			user.set_password(new_password)
			user.save()
			logout(request)
			return redirect("/login/")

	return redirect("/user/profile/")
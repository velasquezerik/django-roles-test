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
from models import UserImage, Folder, File, DiskSpace, Relationship, ShareFolder, LogsFile, LogsFolder, LogsRelationship
from tesis.settings import *
import os
from files_manage import *
import html2text

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
	user = User.objects.get(id = request.user.id)
	root_folder = Folder.objects.get(user_id=user.id,father=0)
	folders = Folder.objects.filter(father=root_folder.id)
	files = File.objects.filter(folder = root_folder.id)
	return render(request,'admin/index.html',{'root_folder':root_folder,'folders':folders, 'files':files})

@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_view(request):
	user = User.objects.get(id = request.user.id)
	root_folder = Folder.objects.get(user_id=user.id,father=0)
	folders = Folder.objects.filter(father=root_folder.id)
	files = File.objects.filter(folder = root_folder.id)
	return render(request,'user/index.html',{'root_folder':root_folder,'folders':folders, 'files':files})


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

		create_root_folder(user.id)

		#create role for user
		assign_role(user, "system_user")

		#create image for user
		image = UserImage()
		image.user = user
		image.save()

		#create DiskSpace
		space = DiskSpace()
		space.user = user
		space.save()


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

		create_root_folder(user.id)

		#create role for user
		assign_role(user, "system_admin")

		#create image for user
		image = UserImage()
		image.user = user
		image.save()

		#create DiskSpace
		space = DiskSpace()
		space.user = user
		space.max_space = 1024
		space.save()

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
		space = request.POST['space']

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

		#update space
		diskspace = DiskSpace.objects.get(user = user.id)
		diskspace.max_space = space
		diskspace.save()

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




def test_folder(request):
	user = User.objects.get(id=request.user.id)

	create_folder(MEDIA_ROOT,user.username)

	return redirect('/')



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_create_folder(request):
	if request.method == "POST":
		user = User.objects.get(id=request.user.id)
		name = request.POST['name']
		father = request.POST['father_id']
		father = Folder.objects.get(id=father)
		user= request.POST['user_id']
		user = User.objects.get(id=user)

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		if diskspace.max_space > diskspace.usage:
			#create folder
			folder_id = create_new_folder(request.POST['user_id'], request.POST['father_id'],request.POST['name'])
			#update space
			diskspace.usage = usage_space(user.id)
			diskspace.save()

			log = LogsFolder()
			log.user = user
			log.folder = Folder.objects.get(id=folder_id)
			log.description = "Create a folder"
			log.save()
		

		if father.father != 0:
			return redirect("/admin/folder/"+str(father.id))
	
	return redirect("/admin/")



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_folder_show(request,folder_id):
	user = User.objects.get(id = request.user.id)
	root_folder = Folder.objects.get(id=folder_id)
	folders = Folder.objects.filter(father=root_folder.id)
	files = File.objects.filter(folder = root_folder.id)
	return render(request,'admin/show_folder.html',{'root_folder':root_folder,'folders':folders,'files':files})




@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_create_folder(request):
	if request.method == "POST":
		user = User.objects.get(id=request.user.id)
		name = request.POST['name']
		father = request.POST['father_id']
		father = Folder.objects.get(id=father)
		user= request.POST['user_id']
		user = User.objects.get(id=user)


		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		if diskspace.max_space > diskspace.usage:
			#create folder
			folder_id = create_new_folder(request.POST['user_id'], request.POST['father_id'],request.POST['name'])
			#update space
			diskspace.usage = usage_space(user.id)
			diskspace.save()

			log = LogsFolder()
			log.user = user
			log.folder = Folder.objects.get(id=folder_id)
			log.description = "Create a folder"
			log.save()
	
		if father.father != 0:
			return redirect("/user/folder/"+str(father.id))

	return redirect("/user/")



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_folder_show(request,folder_id):
	user = User.objects.get(id = request.user.id)
	root_folder = Folder.objects.get(id=folder_id)
	folders = Folder.objects.filter(father=root_folder.id)
	files = File.objects.filter(folder = root_folder.id)
	return render(request,'user/show_folder.html',{'root_folder':root_folder,'folders':folders,'files':files})



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_edit_folder(request):
	if request.method == "POST":
		name = request.POST['name']
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)

		#update folder name
		edit_folder(request.POST['user_id'], request.POST['folder_id'],request.POST['name'])

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		diskspace.usage = usage_space(user.id)
		diskspace.save()

		log = LogsFolder()
		log.user = user
		log.folder = folder
		log.description = "Edit a folder"
		log.save()

		return redirect("/admin/folder/"+str(folder.id))
	
	return redirect("/admin/")



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_edit_folder(request):
	if request.method == "POST":
		name = request.POST['name']
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)

		#update folder name
		edit_folder(request.POST['user_id'], request.POST['folder_id'],request.POST['name'])

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		diskspace.usage = usage_space(user.id)
		diskspace.save()

		log = LogsFolder()
		log.user = user
		log.folder = folder
		log.description = "Edit a folder"
		log.save()

		return redirect("/user/folder/"+str(folder.id))
	
	return redirect("/user/")



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_delete_folder(request):
	if request.method == "POST":
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)
		father = Folder.objects.get(id=folder.father)

		#update folder name
		delete_folder(request.POST['user_id'], request.POST['folder_id'])

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		diskspace.usage = usage_space(user.id)
		diskspace.save()

		if father.father != 0:
			return redirect("/admin/folder/"+str(father.id))

	return redirect("/admin/")



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_delete_folder(request):
	if request.method == "POST":
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)
		father = Folder.objects.get(id=folder.father)

		#update folder name
		delete_folder(request.POST['user_id'], request.POST['folder_id'])

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		diskspace.usage = usage_space(user.id)
		diskspace.save()

		if father.father != 0:
			return redirect("/user/folder/"+str(father.id))

	return redirect("/user/")



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_create_file(request):
	if request.method == "POST":
		name = request.POST['name']
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		if diskspace.max_space > diskspace.usage:
			#create file
			file_id = create_file(request.POST['name'], request.POST['folder_id'])
			#update space
			diskspace.usage = usage_space(user.id)
			diskspace.save()

			#create log file
			log = LogsFile()
			log.user = user
			log.file = File.objects.get(id=file_id)
			log.description = "Create a File"
			log.save()

		

		if folder.father != 0:
			return redirect("/admin/folder/"+str(folder.id))
	
	return redirect("/admin/")


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_create_file(request):
	if request.method == "POST":
		name = request.POST['name']
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)


		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		if diskspace.max_space > diskspace.usage:
			#create file
			file_id = create_file(request.POST['name'], request.POST['folder_id'])
			#update space
			diskspace.usage = usage_space(user.id)
			diskspace.save()

			#create log file
			log = LogsFile()
			log.user = user
			log.file = File.objects.get(id=file_id)
			log.description = "Create a File"
			log.save()


		

		if folder.father != 0:
			return redirect("/user/folder/"+str(folder.id))
	
	return redirect("/user/")




@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_upload_file(request):
	if request.method == "POST":
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)
		file = request.FILES['file']

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		if diskspace.max_space > diskspace.usage:
			#create file
			file_id = upload_file(file.name, request.POST['folder_id'],file)
			#update space
			diskspace.usage = usage_space(user.id)
			diskspace.save()

			#create log file
			log = LogsFile()
			log.user = user
			log.file = File.objects.get(id=file_id)
			log.description = "Upload a File"
			log.save()

		

		if folder.father != 0:
			return redirect("/admin/folder/"+str(folder.id))
	
	return redirect("/admin/")




@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_upload_file(request):
	if request.method == "POST":
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)
		file = request.FILES['file']

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		if diskspace.max_space > diskspace.usage:
			#create file
			file_id = upload_file(file.name, request.POST['folder_id'],file)
			#update space
			diskspace.usage = usage_space(user.id)
			diskspace.save()

			#create log file
			log = LogsFile()
			log.user = user
			log.file = File.objects.get(id=file_id)
			log.description = "Upload a File"
			log.save()


		if folder.father != 0:
			return redirect("/user/folder/"+str(folder.id))
	
	return redirect("/user/")




@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_file_show(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	folder = file.folder
	info = get_file_info(file_id)
	#transfor text to htmls
	info = "<br />".join(info.split("\n"))
	return render(request,'admin/show_file.html',{'folder':folder,'file':file,'info':info})



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_delete_file(request, file_id):
	file = File.objects.get(id=file_id)
	folder = file.folder

	delete_file(file_id)
	file.delete()

	#verify space
	diskspace = DiskSpace.objects.get(user=request.user.id)
	diskspace.usage = usage_space(request.user.id)
	diskspace.save()

	if folder.father != 0:
			return redirect("/admin/folder/"+str(folder.id))
	
	return redirect("/admin/")



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_update_file(request):

	if request.method == "POST":
		file = request.POST['file_id']
		file = File.objects.get(id=file)
		
		info_file = request.POST['info_file']

		data = html2text.html2text(info_file)
		
		update_file(file.id,data)

		#verify space
		diskspace = DiskSpace.objects.get(user=request.user.id)
		diskspace.usage = usage_space(request.user.id)
		diskspace.save()

		#create log file
		log = LogsFile()
		log.user = request.user
		log.file = file
		log.description = "Edit a File"
		log.save()

		return redirect("/admin/file/"+str(file.id))
	return redirect("/admin/")



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_file_show(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	folder = file.folder
	info = get_file_info(file_id)
	#transfor text to htmls
	info = "<br />".join(info.split("\n"))
	return render(request,'user/show_file.html',{'folder':folder,'file':file,'info':info})



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_delete_file(request, file_id):
	file = File.objects.get(id=file_id)
	folder = file.folder

	delete_file(file_id)
	file.delete()

	#verify space
	diskspace = DiskSpace.objects.get(user=request.user.id)
	diskspace.usage = usage_space(request.user.id)
	diskspace.save()

	if folder.father != 0:
			return redirect("/user/folder/"+str(folder.id))
	
	return redirect("/user/")



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_update_file(request):

	if request.method == "POST":
		file = request.POST['file_id']
		file = File.objects.get(id=file)
		
		info_file = request.POST['info_file']

		data = html2text.html2text(info_file)
		
		update_file(file.id,data)

		#verify space
		diskspace = DiskSpace.objects.get(user=request.user.id)
		diskspace.usage = usage_space(request.user.id)
		diskspace.save()

		#create log file
		log = LogsFile()
		log.user = request.user
		log.file = file
		log.description = "Edit a File"
		log.save()

		return redirect("/user/file/"+str(file.id))
	return redirect("/user/")
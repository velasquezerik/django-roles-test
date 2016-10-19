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
from models import UserImage, Folder, File, DiskSpace, Relationship, ShareFolder, ShareFile, LogsFile, LogsFolder, LogsRelationship, LogsShareFile
from tesis.settings import *
import os
from files_manage import *
from galatea_manage import *
import html2text
from django.db.models import Q

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
def admin_show_logs_files(request):
	users = User.objects.all()
	logs = LogsFile.objects.all()
	return render(request,'admin/show_logs_files.html',{'users':users,'logs':logs})

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_show_logs_folders(request):
	users = User.objects.all()
	logs = LogsFolder.objects.all()
	return render(request,'admin/show_logs_folders.html',{'users':users,'logs':logs})

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_show_logs_relations(request):
	users = User.objects.all()
	logs = LogsRelationship.objects.all()
	return render(request,'admin/show_logs_relations.html',{'users':users,'logs':logs})


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
		folders_count = Folder.objects.filter(user_id = user_id).count()
		files_count = File.objects.filter(folder__user_id = user_id).count()
		folders = Folder.objects.filter(user_id = user_id)
		files = File.objects.filter(folder__user_id = user_id)
	except Exception, e:
		return redirect("/admin/users/")

	return render(request,'admin/show_user.html',{'user_show':user,'folders_count':folders_count,'files_count':files_count,'folders':folders,'files':files})


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
def admin_create_project(request):
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


			#create file
			file_id = create_file_project(request.POST['name']+".g", folder_id)
			#update space
			diskspace.usage = usage_space(user.id)
			diskspace.save()

			#create log file
			log = LogsFile()
			log.user = user
			log.file = File.objects.get(id=file_id)
			log.description = "Create a File"
			log.save()



		if father.father != 0:
			return redirect("/admin/folder/"+str(father.id))

	return redirect("/admin/")




@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_create_project(request):
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


			#create file
			file_id = create_file_project(request.POST['name']+".g", folder_id)
			#update space
			diskspace.usage = usage_space(user.id)
			diskspace.save()

			#create log file
			log = LogsFile()
			log.user = user
			log.file = File.objects.get(id=file_id)
			log.description = "Create a File"
			log.save()



		if father.father != 0:
			return redirect("/user/folder/"+str(father.id))

	return redirect("/user/")






@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_folder_show(request,folder_id):
	user = User.objects.get(id = request.user.id)
	root_folder = Folder.objects.get(id=folder_id)
	folders = Folder.objects.filter(father=root_folder.id)
	files = File.objects.filter(folder = root_folder.id)
	all_folders = Folder.objects.filter(user = user.id)
	return render(request,'admin/show_folder.html',{'root_folder':root_folder,'folders':folders,'files':files, 'all_folders':all_folders})



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_folder_share_show(request):
	user = User.objects.get(id = request.user.id)
	files = ShareFile.objects.filter(user=user.id).filter(status=1)
	return render(request,'admin/show_share_folder.html',{'files':files})


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_folder_share_show(request):
	user = User.objects.get(id = request.user.id)
	files = ShareFile.objects.filter(user=user.id).filter(status=1)
	return render(request,'user/show_share_folder.html',{'files':files})




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
	all_folders = Folder.objects.filter(user = user.id)
	return render(request,'user/show_folder.html',{'root_folder':root_folder,'folders':folders,'files':files, 'all_folders':all_folders})



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
@has_role_decorator('system_admin')
def admin_move_folder(request):
	if request.method == "POST":
		new_folder = request.POST['folder_change_id']
		folder = request.POST['folder_id']

		folder = Folder.objects.get(id=folder)
		new_folder = Folder.objects.get(id=new_folder)

		#move folder
		move_folder(folder.id, new_folder.id)

		log = LogsFolder()
		user = User.objects.get(id=request.user.id)
		log.user = user
		log.folder = folder
		log.description = "Move a folder"
		log.save()


		if new_folder.father != 0:
			return redirect("/admin/folder/"+str(new_folder.id))

	return redirect("/admin/")


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_move_file(request):
	if request.method == "POST":
		new_folder = request.POST['folder_change_id']
		file = request.POST['file_id']

		file = File.objects.get(id=file)
		new_folder = Folder.objects.get(id=new_folder)

		#move file
		move_file(file.id, new_folder.id)

		log = LogsFile()
		user = User.objects.get(id=request.user.id)
		log.user = user
		log.file = file
		log.description = "Move a File"
		log.save()

		if new_folder.father != 0:
			return redirect("/admin/folder/"+str(new_folder.id))

	return redirect("/admin/")


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_share_file(request):
	if request.method == "POST":
		user_share = request.POST['user_id']
		user_share = User.objects.get(id=user_share)
		file = request.POST['file_id']
		file = File.objects.get(id=file)


		#share file
		share_file = ShareFile()
		share_file.status = 0
		share_file.file = file
		share_file.user = user_share
		share_file.permission = 2
		share_file.save()

		#create logs
		logs = LogsShareFile()
		logs.share_file = share_file
		logs.description = "User share a file"
		logs.save()


		if file.folder.father != 0:
			return redirect("/admin/folder/"+str(file.folder.id))

	return redirect("/admin/")

@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_share_file(request):
	if request.method == "POST":
		user_share = request.POST['user_id']
		user_share = User.objects.get(id=user_share)
		file = request.POST['file_id']
		file = File.objects.get(id=file)


		#share file
		share_file = ShareFile()
		share_file.status = 0
		share_file.file = file
		share_file.user = user_share
		share_file.permission = 2
		share_file.save()

		#create logs
		logs = LogsShareFile()
		logs.share_file = share_file
		logs.description = "User share a file"
		logs.save()


		if file.folder.father != 0:
			return redirect("/user/folder/"+str(file.folder.id))

	return redirect("/user/")


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_move_file(request):
	if request.method == "POST":
		new_folder = request.POST['folder_change_id']
		file = request.POST['file_id']

		file = File.objects.get(id=file)
		new_folder = Folder.objects.get(id=new_folder)

		#move file
		move_file(file.id, new_folder.id)

		log = LogsFile()
		user = User.objects.get(id=request.user.id)
		log.user = user
		log.file = file
		log.description = "Move a File"
		log.save()

		if new_folder.father != 0:
			return redirect("/user/folder/"+str(new_folder.id))

	return redirect("/user/")



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_move_folder(request):
	if request.method == "POST":
		new_folder = request.POST['folder_change_id']
		folder = request.POST['folder_id']

		folder = Folder.objects.get(id=folder)
		new_folder = Folder.objects.get(id=new_folder)

		#move folder
		move_folder(folder.id, new_folder.id)

		log = LogsFolder()
		user = User.objects.get(id=request.user.id)
		log.user = user
		log.folder = folder
		log.description = "Move a folder"
		log.save()


		if new_folder.father != 0:
			return redirect("/user/folder/"+str(new_folder.id))

	return redirect("/user/")



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
@has_role_decorator('system_admin')
def admin_result_create_file(request):
	if request.method == "POST":
		name = request.POST['name']
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)
		data = request.POST['data_execution']

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		if diskspace.max_space > diskspace.usage:
			#create file
			file_id = create_file_execution(request.POST['name'], request.POST['folder_id'], data)
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
@has_role_decorator('system_user')
def user_result_create_file(request):
	if request.method == "POST":
		name = request.POST['name']
		folder = request.POST['folder_id']
		folder = Folder.objects.get(id=folder)
		user= request.POST['user_id']
		user = User.objects.get(id=user)
		data = request.POST['data_execution']

		#verify space
		diskspace = DiskSpace.objects.get(user=user.id)
		if diskspace.max_space > diskspace.usage:
			#create file
			file_id = create_file_execution(request.POST['name'], request.POST['folder_id'], data)
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
	all_folders = Folder.objects.filter(user_id = user.id)
	friends = Relationship.objects.filter(Q(user_one=user.id) | Q(user_two=user.id) ).filter(status=1)
	help_code = execute_java_help(file_id)
	#transfor text to htmls
	info = "<br />".join(info.split("\n"))
	extension = os.path.splitext(file.name)[1]
	return render(request,'admin/show_file.html',{'folder':folder,'file':file,'info':info,'all_folders':all_folders,'friends':friends,'help_code':help_code,'extension':extension})

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_file_permission_show(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)

	share_files = ShareFile.objects.filter(file_id = file_id)

	return render(request,'admin/show_file_permission.html',{'file':file,'share_files':share_files})



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_permission_private_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	file.permission = 0;
	file.save()

	return redirect("/admin/permission/file/"+file_id)

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_permission_show_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	file.permission = 1;
	file.save()

	return redirect("/admin/permission/file/"+file_id)

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_permission_edit_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	file.permission = 2;
	file.save()

	return redirect("/admin/permission/file/"+file_id)



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_permission_private_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	file.permission = 0;
	file.save()

	return redirect("/user/permission/file/"+file_id)

@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_permission_show_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	file.permission = 1;
	file.save()

	return redirect("/user/permission/file/"+file_id)

@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_permission_edit_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	file.permission = 2;
	file.save()

	return redirect("/user/permission/file/"+file_id)



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_permission_share_private_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	share = ShareFile.objects.get(id = file_id)
	file = share.file
	share.delete()

	return redirect("/admin/permission/file/"+str(file.id))

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_permission_share_show_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	share = ShareFile.objects.get(id = file_id)
	file = share.file
	share.permission = 1;
	share.save()

	return redirect("/admin/permission/file/"+str(file.id))

@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_permission_share_edit_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	share = ShareFile.objects.get(id = file_id)
	file = share.file
	share.permission = 2;
	share.save()

	return redirect("/admin/permission/file/"+str(file.id))





@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_permission_share_private_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	share = ShareFile.objects.get(id = file_id)
	file = share.file
	share.delete()

	return redirect("/user/permission/file/"+str(file.id))

@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_permission_share_show_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	share = ShareFile.objects.get(id = file_id)
	file = share.file
	share.permission = 1;
	share.save()

	return redirect("/user/permission/file/"+str(file.id))

@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_permission_share_edit_file(request,file_id):
	user = User.objects.get(id = request.user.id)
	share = ShareFile.objects.get(id = file_id)
	file = share.file
	share.permission = 2;
	share.save()

	return redirect("/user/permission/file/"+str(file.id))






@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_file_permission_show(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)

	share_files = ShareFile.objects.filter(file_id = file_id)

	return render(request,'user/show_file_permission.html',{'file':file,'share_files':share_files})



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_share_file_show(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	folder = file.folder
	info = get_file_info(file_id)
	all_folders = Folder.objects.filter(user_id = user.id)
	friends = Relationship.objects.filter(Q(user_one=user.id) | Q(user_two=user.id) ).filter(status=1)
	help_code = execute_java_help(file_id)
	share = ShareFile.objects.filter(user_id = user.id).filter(file_id = file_id)[0]
	root_folder = Folder.objects.get(user_id=user.id,father=0)
	#transfor text to htmls
	info = "<br />".join(info.split("\n"))
	extension = os.path.splitext(file.name)[1]
	return render(request,'admin/show_share_file.html',{'folder':folder,'file':file,'info':info,'all_folders':all_folders,'friends':friends,'help_code':help_code,'share':share,'root_folder':root_folder,'extension':extension})


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_share_file_show(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	folder = file.folder
	info = get_file_info(file_id)
	all_folders = Folder.objects.filter(user_id = user.id)
	friends = Relationship.objects.filter(Q(user_one=user.id) | Q(user_two=user.id) ).filter(status=1)
	help_code = execute_java_help(file_id)
	share = ShareFile.objects.filter(user_id = user.id).filter(file_id = file_id)[0]
	root_folder = Folder.objects.get(user_id=user.id,father=0)
	#transfor text to htmls
	info = "<br />".join(info.split("\n"))
	extension = os.path.splitext(file.name)[1]
	return render(request,'user/show_share_file.html',{'folder':folder,'file':file,'info':info,'all_folders':all_folders,'friends':friends,'help_code':help_code,'share':share,'root_folder':root_folder,'extension':extension})



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
@has_role_decorator('system_admin')
def admin_update_share(request):

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

		return redirect("/admin/share/file/"+str(file.id))
	return redirect("/admin/")




@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_update_share(request):

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

		return redirect("/user/share/file/"+str(file.id))
	return redirect("/user/")




@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_file_show(request,file_id):
	user = User.objects.get(id = request.user.id)
	file = File.objects.get(id=file_id)
	folder = file.folder
	info = get_file_info(file_id)
	all_folders = Folder.objects.filter(user_id = user.id)
	friends = Relationship.objects.filter(Q(user_one=user.id) | Q(user_two=user.id) ).filter(status=1)
	help_code = execute_java_help(file_id)
	#transfor text to htmls
	info = "<br />".join(info.split("\n"))
	extension = os.path.splitext(file.name)[1]
	return render(request,'user/show_file.html',{'folder':folder,'file':file,'info':info,'all_folders':all_folders,'friends':friends,'help_code':help_code,'extension':extension})



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



def run_test(request):
	test_process()
	traslate = traslate_java(1)
	com_java = compile_java(1)
	exe_java = execute_java(1)
	return redirect("/user/")



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_compile_file(request, file_id):
	file = File.objects.get(id=file_id)

	com_java = compile_java(file.id)

	return JsonResponse({"data":com_java})




@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_execute_file(request, file_id):
	#get arguments for compilation
	arguments =  request.GET['arguments']
	file = File.objects.get(id=file_id)

	com_java = execute_java(file.id, arguments)

	return JsonResponse({"data":com_java})



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_compile_file(request, file_id):
	file = File.objects.get(id=file_id)

	com_java = compile_java(file.id)

	return JsonResponse({"data":com_java})




@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_execute_file(request, file_id):
	#get arguments for compilation
	arguments =  request.GET['arguments']
	file = File.objects.get(id=file_id)

	com_java = execute_java(file.id, arguments)

	return JsonResponse({"data":com_java})




@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_friends(request):
	user = User.objects.get(id = request.user.id)

	friends = Relationship.objects.filter(Q(user_one=user.id) | Q(user_two=user.id) ).filter(status=1)

	return render(request,'admin/show_friends.html',{'friends':friends})



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_friends(request):
	user = User.objects.get(id = request.user.id)

	friends = Relationship.objects.filter(Q(user_one=user.id) | Q(user_two=user.id)).filter(status=1)

	return render(request,'user/show_friends.html',{'friends':friends})



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_get_friends(request):
	user = User.objects.get(id = request.user.id)

	users = User.objects.all().exclude(id=user.id)

	friends = Relationship.objects.filter(Q(user_one=user.id) | Q(user_two=user.id))

	for xuser in users:
		for friend in friends:
			if xuser.id == friend.user_one.id  or xuser.id == friend.user_two.id:
				users = users.exclude(id=xuser.id)

	return render(request,'admin/get_friends.html',{'users':users})



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_send_friend_request(request, user_id):
	user = User.objects.get(id = request.user.id)
	friend = User.objects.get(id=user_id)

	friends = Relationship.objects.filter(user_one=user.id).filter(user_two=friend.id).count()
	print friends
	if friends > 0:
		return redirect("/admin/")

	friends = Relationship.objects.filter(user_one=friend.id).filter(user_two=user.id).count()
	print friends
	if friends > 0:
		return redirect("/admin/")

	#create relationship
	relation = Relationship()
	relation.status = 0
	relation.user_one = user
	relation.user_two = friend
	relation.save()

	#create logs
	log = LogsRelationship()
	log.relationship = relation
	log.description = "Send friendship request"
	log.save()

	return redirect("/admin/get_friends/")




@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_get_friends(request):
	user = User.objects.get(id = request.user.id)

	users = User.objects.all().exclude(id=user.id)

	friends = Relationship.objects.filter(Q(user_one=user.id) | Q(user_two=user.id))

	for xuser in users:
		for friend in friends:
			if xuser.id == friend.user_one.id  or xuser.id == friend.user_two.id:
				users = users.exclude(id=xuser.id)

	return render(request,'user/get_friends.html',{'users':users})



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_send_friend_request(request, user_id):
	user = User.objects.get(id = request.user.id)
	friend = User.objects.get(id=user_id)

	friends = Relationship.objects.filter(user_one=user.id).filter(user_two=friend.id).count()
	print friends
	if friends > 0:
		return redirect("/user/")

	friends = Relationship.objects.filter(user_one=friend.id).filter(user_two=user.id).count()
	print friends
	if friends > 0:
		return redirect("/user/")

	#create relationship
	relation = Relationship()
	relation.status = 0
	relation.user_one = user
	relation.user_two = friend
	relation.save()

	#create logs
	log = LogsRelationship()
	log.relationship = relation
	log.description = "Send friendship request"
	log.save()

	return redirect("/user/get_friends/")





@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_friends_notifications(request):
	user = User.objects.get(id = request.user.id)

	friends = Relationship.objects.filter(user_two=user.id).filter(status=0)

	return render(request,'admin/friend_notification.html',{'friends':friends})


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_share_files_notifications(request):
	user = User.objects.get(id = request.user.id)

	share_files = ShareFile.objects.filter(user = user.id).filter(status=0)

	return render(request,'admin/share_files_notification.html',{'share_files':share_files})


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_share_files_notifications(request):
	user = User.objects.get(id = request.user.id)

	share_files = ShareFile.objects.filter(user = user.id).filter(status=0)

	return render(request,'user/share_files_notification.html',{'share_files':share_files})





@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_accept_friend_request(request, request_id):
	user = User.objects.get(id = request.user.id)
	relation = Relationship.objects.get(id=request_id)

	relation.status = 1
	relation.save()

	#create logs
	log = LogsRelationship()
	log.relationship = relation
	log.description = "Accepted friendship request"
	log.save()

	return redirect("/admin/friends/")



@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_accept_share_files_request(request, request_id):
	user = User.objects.get(id = request.user.id)
	share_file = ShareFile.objects.get(id=request_id)

	share_file.status = 1
	share_file.save()

	#create logs
	log = LogsShareFile()
	log.share_file = share_file
	log.description = "Accepted share file request"
	log.save()

	return redirect("/admin/notifications_share_files/")


@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_denied_share_files_request(request, request_id):
	user = User.objects.get(id = request.user.id)
	share_file = ShareFile.objects.get(id=request_id)

	share_file.status = 2
	share_file.save()

	#create logs
	log = LogsShareFile()
	log.share_file = share_file
	log.description = "Denied share file request"
	log.save()

	return redirect("/admin/notifications_share_files/")



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_accept_share_files_request(request, request_id):
	user = User.objects.get(id = request.user.id)
	share_file = ShareFile.objects.get(id=request_id)

	share_file.status = 1
	share_file.save()

	#create logs
	log = LogsShareFile()
	log.share_file = share_file
	log.description = "Accepted share file request"
	log.save()

	return redirect("/user/notifications_share_files/")


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_denied_share_files_request(request, request_id):
	user = User.objects.get(id = request.user.id)
	share_file = ShareFile.objects.get(id=request_id)

	share_file.status = 2
	share_file.save()

	#create logs
	log = LogsShareFile()
	log.share_file = share_file
	log.description = "Denied share file request"
	log.save()

	return redirect("/user/notifications_share_files/")




@login_required(login_url="/login/")
@has_role_decorator('system_admin')
def admin_denied_friend_request(request, request_id):
	user = User.objects.get(id = request.user.id)
	relation = Relationship.objects.get(id=request_id)

	relation.status = 2
	relation.save()

	#create logs
	log = LogsRelationship()
	log.relationship = relation
	log.description = "Denied friendship request"
	log.save()

	return redirect("/admin/friends/")


@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_friends_notifications(request):
	user = User.objects.get(id = request.user.id)

	friends = Relationship.objects.filter(user_two=user.id).filter(status=0)

	return render(request,'user/friend_notification.html',{'friends':friends})



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_accept_friend_request(request, request_id):
	user = User.objects.get(id = request.user.id)
	relation = Relationship.objects.get(id=request_id)

	relation.status = 1
	relation.save()

	#create logs
	log = LogsRelationship()
	log.relationship = relation
	log.description = "Accepted friendship request"
	log.save()

	return redirect("/user/friends/")



@login_required(login_url="/login/")
@has_role_decorator('system_user')
def user_denied_friend_request(request, request_id):
	user = User.objects.get(id = request.user.id)
	relation = Relationship.objects.get(id=request_id)

	relation.status = 2
	relation.save()

	#create logs
	log = LogsRelationship()
	log.relationship = relation
	log.description = "Denied friendship request"
	log.save()

	return redirect("/user/friends/")

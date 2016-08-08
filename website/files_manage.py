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
from models import UserImage, Folder
from tesis.settings import *
from os import *


#create folder
def create_folder(root, name):
	directory = root +"/"+ name
	print directory
	if not path.exists(directory):
		try:
			makedirs(directory)
		except Exception, e:
			return False
		else:
			return True
		

#create folder
def create_root_folder(user_id):
	root = MEDIA_ROOT
	user = User.objects.get(id=user_id)
	directory = root +"/"+ user.username
	print directory
	if not path.exists(directory):
		try:
			folder = Folder()
			folder.name = user.username
			folder.path = directory
			folder.user = user
			folder.save()
			makedirs(directory)
		except Exception, e:
			return False
		else:
			return True
		

#create new folder
def create_new_folder(user_id,father_id,name):
	root = MEDIA_ROOT
	user = User.objects.get(id=user_id)
	father = Folder.objects.get(id=father_id)
	directory = father.path +"/"+ name
	print directory
	if not path.exists(directory):
		try:
			folder = Folder()
			folder.name = name
			folder.path = directory
			folder.user = user
			folder.father = father.id
			folder.active = True
			folder.save()
			makedirs(directory)
		except Exception, e:
			return False
		else:
			return True




"""
    <GALATEA WEB: Web system simulations>
    Copyright (C) 2016  Erik Velasquez erikvelasquez.25@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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
from models import UserImage, Folder, File
from tesis.settings import *
import os
import shutil

INITIAL_DATA = 'Example Project\n   Incoming persons arrive at a bank teller at interarrival times\n    taken at random from an exponential distribution with mean\n    <<InArrTime>>. They are served one at a time. Serving times are\n   taken from a gaussian distribution with mean <<MeSerTime>> and\n   standard deviation <<DeSerTime>>.\n    Have the model ready to change the parameters (<<INTI>> Instructions).\nTITLE\n Example Project\nNETWORK\n   Gate (I){\n        IT=EXPO(InArrTime);\n       WRITE("ARRIVE:\t" + TIME);\n       ACT(ShowLength,0);\n       SENDTO(Teller);\n  }\n   Teller (R){\n      STAY=GAUSS(MeSerTime,DeSerTime);\n        RELEASE\nSENDTO(Exit);\n    }\n Exit (E) {\n     WRITE("EXIT:\t" + TIME);\n       ACT(ShowLength,0);\n   }\n    ShowLength (A) {\n      WRITELN("\tthere are " + LL(Teller.el) + " clients waiting ");\n  }\nINIT\n TSIM = 10;\n ACT(Gate,0);\n   /* To modify parameters during INIT execution*/\n  INTI(InArrTime, 4.0, "Mean Interarrival Time");\n INTI(MeSerTime, 3.50, "Mean service time");\n    INTI(DeSerTime, 0.80, "Deviation of Mean Service Time");\nDECL\n    REAL InArrTime,MeSerTime,DeSerTime; \nEND.'

"""
Simple Teller
    Incoming persons arrive at a bank teller at interarrival times
    taken at random from an exponential distribution with mean
    <<InArrTime>>. They are served one at a time. Serving times are
    taken from a gaussian distribution with mean <<MeSerTime>> and
    standard deviation <<DeSerTime>>.
    Have the model ready to change the parameters (<<INTI>> Instructions).
TITLE
    Simple Teller
NETWORK
    Gate (I){
        IT=EXPO(InArrTime);
        WRITE("ARRIVE:\t" + TIME);
        ACT(ShowLength,0);
        SENDTO(Teller);
    }
    Teller (R){
        STAY=GAUSS(MeSerTime,DeSerTime);
        RELEASE
            SENDTO(Exit);
    }
    Exit (E) {
        WRITE("EXIT:\t" + TIME);
        ACT(ShowLength,0);
    }
    ShowLength (A) {
        WRITELN("\tthere are " + LL(Teller.el) + " clients waiting ");
    }
INIT
    TSIM = 10;
    ACT(Gate,0);

    /* To modify parameters during INIT execution*/
    INTI(InArrTime, 4.0, "Mean Interarrival Time");
    INTI(MeSerTime, 3.50, "Mean service time");
    INTI(DeSerTime, 0.80, "Deviation of Mean Service Time");
DECL
    REAL InArrTime,MeSerTime,DeSerTime;
END. """

#create folder
def create_folder(root, name):
	directory = root +"/"+ name
	print directory
	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
		except Exception, e:
			return False
		else:
			return True


#get usage from folder
def usage_space(user_id):
	root = MEDIA_ROOT
	user = User.objects.get(id=user_id)
	directory = root +"/"+ user.username
	start_path = directory
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	return (total_size/1024)/1024

#create folder
def create_root_folder(user_id):
	root = MEDIA_ROOT
	user = User.objects.get(id=user_id)
	directory = root +"/"+ user.username
	print directory
	if not os.path.exists(directory):
		try:
			folder = Folder()
			folder.name = user.username
			folder.path = directory
			folder.user = user
			folder.save()
			os.makedirs(directory)
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
	id_folder = 0
	print directory
	if not os.path.exists(directory):
		try:
			folder = Folder()
			folder.name = name
			folder.path = directory
			folder.user = user
			folder.father = father.id
			folder.active = True
			folder.save()
			id_folder = folder.id
			os.makedirs(directory)
		except Exception, e:
			return id_folder
		else:
			return id_folder

#create new folder
def edit_folder(user_id,folder_id,name):
	root = MEDIA_ROOT
	user = User.objects.get(id=user_id)
	folder = Folder.objects.get(id=folder_id)
	father = Folder.objects.get(id=folder.father)
	directory = father.path +"/"+ name

	os.rename(folder.path,directory)

	folder.name = name
	folder.path = directory
	folder.save()
	return True



#delete folder
def delete_folder(user_id, folder_id):
	root = MEDIA_ROOT
	user = User.objects.get(id=user_id)
	folder = Folder.objects.get(id=folder_id)
	father = Folder.objects.get(id=folder.father)
	directory = father.path +"/"+ folder.name

	shutil.rmtree(folder.path)

	folder.delete()

	return True

#update all paths
def update_path_folders(folder_id , father_id):
	father = Folder.objects.get(id=father_id)
	folder = Folder.objects.get(id=folder_id)
	folder.father = father.id
	folder.path = father.path +"/"+ folder.name
	folder.save()

	#get all children
	folders = Folder.objects.filter(father=folder.id)
	for fol in folders:
		update_path_folders(fol.id, folder.id)


#move folder
def move_folder(folder_id, new_folder_id):
	root = MEDIA_ROOT
	folder = Folder.objects.get(id=folder_id)
	if folder.father != new_folder_id:
		new_folder = Folder.objects.get(id=new_folder_id)

		shutil.move(folder.path, new_folder.path)

		#update all paths
		update_path_folders(folder.id,new_folder.id)

		"""folder.father = new_folder.id
		folder.path = new_folder.path +"/"+ folder.name
		folder.save()"""

	return True


#move file
def move_file(file_id, new_folder_id):
	root = MEDIA_ROOT
	file = File.objects.get(id=file_id)
	new_folder = Folder.objects.get(id=new_folder_id)

	shutil.move(file.folder.path + "/" + file.name, new_folder.path + "/" + file.name)

	file.folder = new_folder
	file.save()

	return True

#create new file
def create_file(name, folder_id):
	root = MEDIA_ROOT
	folder = Folder.objects.get(id=folder_id)
	# Open a file
	f = open(folder.path + "/" + name, "w")
	# Close opend file
	f.close()

	file = File()
	file.name = name
	file.folder = folder
	file.active = True
	file.save()

	return file.id

#create new file
def create_file_project(name, folder_id):
	root = MEDIA_ROOT
	folder = Folder.objects.get(id=folder_id)
	# Open a file
	f = open(folder.path + "/" + name  , "w")
	f.write(INITIAL_DATA)
	# Close opend file
	f.close()

	file = File()
	file.name = name
	file.folder = folder
	file.active = True
	file.save()

	return file.id

#create new file
def create_file_execution(name, folder_id, data):
	root = MEDIA_ROOT
	folder = Folder.objects.get(id=folder_id)
	# Open a file
	f = open(folder.path + "/" + name, "w")
	f.write(data)
	# Close opend file
	f.close()

	file = File()
	file.name = name
	file.folder = folder
	file.active = True
	file.save()

	return file.id

#upload files
def upload_file(name, folder_id, f):
	root = MEDIA_ROOT
	folder = Folder.objects.get(id=folder_id)
	# create a file
	with open(folder.path + "/" + name, 'w') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

	file = File()
	file.name = name
	file.folder = folder
	file.active = True
	file.save()

	return file.id


#get file info
def get_file_info(file_id):
	file = File.objects.get(id = file_id)
	f = open(file.folder.path + "/" + file.name, 'r')
	data = f.read()
	f.close()
	return data


#delete a file
def delete_file(file_id):
	file = File.objects.get(id=file_id)
	os.remove(file.folder.path+"/"+file.name)
	return True

#update file
def update_file(file_id,data):
	file = File.objects.get(id=file_id)
	f = open(file.folder.path + "/" + file.name, "w")
	f.write(data)
	f.close()
	return True

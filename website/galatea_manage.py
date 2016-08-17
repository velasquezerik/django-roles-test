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
import subprocess


def test_process():
	#java -cp ../../galatea.jar:../../lib/java-cup-11a-runtime.jar galatea.gcompiler.G2Java SimpleTeller.g
	#javac -cp ../../galatea.jar *.java
	#java -cp .:../../galatea.jar SimpleTeller
	value = subprocess.call(["ls", "-l", "/dev/null"], shell=True)
	print value
	return value


#To translate a GALATEA model to Java language
#java -cp ../../galatea.jar:../../lib/java-cup-11a-runtime.jar galatea.gcompiler.G2Java SimpleTeller.g
def traslate_java(file_id):
	file = File.objects.get(id=file_id)
	folder = file.folder
	galatea_code = GALATEA + "galatea.jar:"
	galatea_runtime = GALATEA + "lib/java-cup-11a-runtime.jar galatea.gcompiler.G2Java "
	code = "java -cp "+ galatea_code + galatea_runtime + folder.path + "/" + file.name
	#print code
	value = subprocess.call([code], shell=True)
	#print value
	return value


#compile Java files
#javac -cp ../../galatea.jar *.java
def compile_java(file_id):
	#first traslate
	traslate_java(file_id)

	file = File.objects.get(id=file_id)
	folder = file.folder
	galatea_code = GALATEA + "galatea.jar "
	code = "javac -cp "+ galatea_code + folder.path + "/*.java"
	#print code
	value = subprocess.check_output([code], shell=True)
	#print value
	return value

#run the program
#java -cp .:../../galatea.jar SimpleTeller
def execute_java(file_id):
	#first compile
	compile_java(file_id)
	file = File.objects.get(id=file_id)
	folder = file.folder
	galatea_code = GALATEA + "galatea.jar "
	#print os.path.splitext(file.name)[0]
	code = "cd "+file.folder.path+" && java -cp .:"+ galatea_code + os.path.splitext(file.name)[0]
	#print code
	value = subprocess.check_output([code], shell=True)
	#print value
	return value
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
import subprocess

PORT = 5000

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
    user = folder.user
    galatea_code = GALATEA + "galatea.jar "
    code = "javac -cp "+ galatea_code + folder.path + "/*.java"
    #print code
    value = subprocess.check_output([code], shell=True)
    #print value

    #get all the file in this folder
    for root, dirs, files in os.walk(folder.path):
        root_folder = Folder.objects.get(path=root, name = os.path.basename(root))
        for dir in dirs:
            folders = Folder.objects.filter(father=root_folder.id)
            esta = False
            for folder in folders:
                if folder.name == dir:
                    esta = True
            if not esta:
                folder = Folder()
                folder.name = dir
                folder.path = root_folder.path + "/" + dir
                folder.user = user
                folder.father = root_folder.id
                folder.active = True
                folder.save()
        #print dirs
        for file in files:
            files_folder = File.objects.filter(folder = root_folder.id)
            esta = False
            for f in files_folder:
                if f.name == file:
                    esta = True
            if not esta:
                if (os.path.splitext(file)[1] != ".class"):
                    f = File()
                    f.name = file
                    f.folder = root_folder
                    f.active = True
                    f.save()

    return value

#run the program
#java -cp .:../../galatea.jar SimpleTeller
def execute_java(file_id, arguments):
    #get file
    file = File.objects.get(id=file_id)
    #first compile
    compile_java(file_id)
    folder = file.folder
    galatea_code = GALATEA + "galatea.jar "
    #print os.path.splitext(file.name)[0]
    code = "cd "+file.folder.path+" && java -cp .:"+ galatea_code + os.path.splitext(file.name)[0] + " " + arguments
    #print code
    value = subprocess.check_output([code], shell=True)
    #print value

    #get all the file in this folder
    for root, dirs, files in os.walk(folder.path):
        root_folder = Folder.objects.get(path=root, name = os.path.basename(root))
        for dir in dirs:
            folders = Folder.objects.filter(father=root_folder.id)
            esta = False
            for folder in folders:
                if folder.name == dir:
                    esta = True
            if not esta:
                folder = Folder()
                folder.name = dir
                folder.path = root_folder.path + "/" + dir
                folder.user = user
                folder.father = root_folder.id
                folder.active = True
                folder.save()
        #print dirs
        for file in files:
            files_folder = File.objects.filter(folder = root_folder.id)
            esta = False
            for f in files_folder:
                if f.name == file:
                    esta = True
            if not esta:
                if (os.path.splitext(file)[1] != ".class"):
                    f = File()
                    f.name = file
                    f.folder = root_folder
                    f.active = True
                    f.save()

    return value


#run help the program
#java -cp .:../../galatea.jar SimpleTeller
def execute_java_help(file_id):
    #get file
    file = File.objects.get(id=file_id)
    #check if file exists
    if os.path.exists(file.folder.path + "/help.txt"):
        f = open(file.folder.path + "/help.txt", 'r')
        data = f.read()
        f.close()
        return data

    #first compile
    compile_java(file_id)
    folder = file.folder
    galatea_code = GALATEA + "galatea.jar "
    #print os.path.splitext(file.name)[0]
    code = "cd "+file.folder.path+" && java -cp .:"+ galatea_code + os.path.splitext(file.name)[0] + " -h "
    #print code
    value = subprocess.check_output([code], shell=True)
    #print value
    # create a file
    with open(file.folder.path + "/help.txt", 'w') as destination:
        destination.write(value)
    return value




#run the program
#javac -cp ../../galatea.jar *.java
#java -cp .:../../galatea.jar TCPServer
def execute_integration(arguments):

    #path to GALATEA
    galatea_code = GALATEA + "galatea.jar"
    #path to TCPServer
    #server_code = INTEGRATION_SERVER + "TCPServer "
    server_code = "TCPServer "

    #code to compile
    code = "cd "+INTEGRATION_SERVER+" && javac -cp .:"+ galatea_code+" " + " *.java "
    value = subprocess.check_output([code], shell=True)

    #code to execute
    code = "cd "+INTEGRATION_SERVER+" && java -cp .:"+ galatea_code+" " + server_code + " " + str(PORT) + " " + arguments
    #value = subprocess.check_output([code], shell=True)
    value = subprocess.call([code], shell=True)
    #print value
    return value

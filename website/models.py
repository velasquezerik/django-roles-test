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
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


Private = 0
Show = 1
Edit = 2
Delete = 3
STATUS_PERMISSION = ((Private, 'Private'),(Show, 'Show'),(Edit, 'Edit'),(Delete,'Delete'))


# Create your models here.
class UserImage(models.Model):
	model_pic = models.ImageField(upload_to = 'profiles/', default = 'profiles/profile.png')
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)

#folder model
class Folder(models.Model):
	user =  models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	path = models.CharField(max_length=1000)
	father = models.IntegerField(default=0)
	active = models.BooleanField(default=True)
	permission = models.IntegerField(default=0, choices=STATUS_PERMISSION)


#file model
class File(models.Model):
	"""Atributes"""
	folder =  models.ForeignKey(Folder, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	active = models.BooleanField(default=True)
	permission = models.IntegerField(default=0, choices=STATUS_PERMISSION)


#disk space for users
class DiskSpace(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
	#max space in MB
	max_space = models.IntegerField(default=512)
	usage = models.IntegerField(default=0)


Pending = 0
Accepted = 1
Denied = 2
Removed = 3
STATUS_CHOICES = ((Pending, 'Pending'),(Accepted, 'Accepted'),(Denied, 'Denied'),(Removed,'Removed'))

#relationship for friends
class Relationship(models.Model):
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	user_one =  models.ForeignKey(User,related_name='user_one', on_delete=models.CASCADE)
	user_two =  models.ForeignKey(User,related_name='user_two', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user_one', 'user_two',)



#share folders
class ShareFolder(models.Model):
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
	permission = models.IntegerField(default=0, choices=STATUS_PERMISSION)

	class Meta:
		unique_together = ('user', 'folder',)

#share folders
class ShareFile(models.Model):
	status = models.IntegerField(default=0, choices=STATUS_CHOICES)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	file = models.ForeignKey(File, on_delete=models.CASCADE)
	permission = models.IntegerField(default=0, choices=STATUS_PERMISSION)

	class Meta:
		unique_together = ('user', 'file',)


#logs for relationship
class LogsRelationship(models.Model):
	relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	date = models.DateTimeField(default=datetime.now)


#logs for folders
class LogsFolder(models.Model):
	folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
	user =  models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	date = models.DateTimeField(default=datetime.now)


#logs for files
class LogsFile(models.Model):
	file = models.ForeignKey(File, on_delete=models.CASCADE)
	user =  models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	date = models.DateTimeField(default=datetime.now)



#logs for share folders
class LogsShareFolder(models.Model):
	share_folder = models.ForeignKey(ShareFolder, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	date = models.DateTimeField(default=datetime.now)


#logs for share files
class LogsShareFile(models.Model):
	share_file = models.ForeignKey(ShareFile, on_delete=models.CASCADE)
	description = models.CharField(max_length=1000)
	date = models.DateTimeField(default=datetime.now)

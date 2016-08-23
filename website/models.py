from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

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
		

#file model
class File(models.Model):
	"""Atributes"""
	folder =  models.ForeignKey(Folder, on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	active = models.BooleanField(default=True)


#disk space for users
class DiskSpace(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
	#max space in MB
	max_space = models.IntegerField(default=512)
	usage = models.IntegerField(default=0)


Pending = 0
Accepted = 1
Declined = 2
Blocked = 3
#status model-> Pending, Accepted, Declined, Blocked
STATUS_CHOICES = ((Pending, 'Pending'),(Accepted, 'Accepted'),(Declined, 'Declined'),(Blocked,'Blocked'))

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

	class Meta:
		unique_together = ('user', 'folder',)


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


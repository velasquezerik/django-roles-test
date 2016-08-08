from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

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
		
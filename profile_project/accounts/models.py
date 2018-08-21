from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.db import models
from django.db.models.signals import post_save
from smartfields import fields

#https://stackoverflow.com/questions/42075882/manager-object-has-no-attribute-get-by-natural-key?rq=1
class UserAccountManager(BaseUserManager):
	'''Model for the account manager relation.'''
	def create_user(self, first_name, last_name, email,
					username=None, password=None):
		if not email:
			raise ValueError('All Users have to have an email')
		if not username:
			raise ValueError('All Users have to have a username.')
		user = self.model(first_name=first_name, 
							last_name=last_name,
							email=email,
							username=username)
		user.set_password(password)
		user.save()
		return user

class User(AbstractBaseUser):
	'''Model for the User relation.'''
	first_name = models.CharField(max_length=25, blank=True)
	last_name = models.CharField(max_length=25, blank=True)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(blank=True)
	
	objects = UserAccountManager()
	
	USERNAME_FIELD = 'username'

def min_length(value):
	if len(value) < 10:
		raise ValidationError('Entered field must be ' +
								'longer than 10 characters.')

class Profile(models.Model):
	'''Model for the user profile. Maintains a 'one-to-one'
	relationship with the User relation.'''
	user = models.OneToOneField('User', on_delete=models.CASCADE)
	birthdate = models.DateField(blank=True, null=True)
	bio = models.TextField(blank=True, null=True)
	#https://django-smartfields.readthedocs.io/en/latest/
	avatar = models.ImageField(upload_to='avatar_photos/', blank=True, null=True)
	
	def __str__(self):
		return self.user.first_name
		
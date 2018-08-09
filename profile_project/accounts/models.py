from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.db import models

#https://stackoverflow.com/questions/42075882/manager-object-has-no-attribute-get-by-natural-key?rq=1
class UserAccountManager(BaseUserManager):
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
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField()
	
	objects = UserAccountManager()
	
	USERNAME_FIELD = 'username'

def min_length(value):
	if len(value) < 10:
		raise ValidationError('Entered field must be ' +
								'longer than 10 characters.')

# Create your models here.
class Profile(models.Model):
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField()
	password = models.CharField(max_length=25)
	birthdate = models.DateField()
	bio = models.TextField(validators=[min_length])
	avatar = models.NullBooleanField(null=True)
	
	USERNAME_FIELD = 'username'
	
	
	def __str__(self):
		return self.first_name
		

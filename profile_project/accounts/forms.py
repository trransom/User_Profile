from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from . import models

class CreateUserForm(UserCreationForm):
	class Meta:
		model = models.User
		fields = ['username']
		
class UpdateUserForm(forms.ModelForm):
	class Meta:
		model = models.User
		fields = ['first_name', 'last_name', 'username', 'email']
		
class UpdateProfileForm(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['birthdate', 'bio']


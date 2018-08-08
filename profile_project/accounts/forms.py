from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from . import models

class CreateUserForm(UserCreationForm):
	class Meta:
		model = models.User
		fields = ['username']


#class AuthenticationForm(forms.ModelForm):
#	class Meta:
#		model = Profile
#		fields = ['username', 'password']
#		exclude = ['firstname', 'lastname', 'email', 'birthdate',
#					'bio', 'avatar']
from django import forms

from .models import Profile

class UserCreationForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['firstname', 'lastname', 'email', 'password', 'birthdate', 'avatar']


class AuthenticationForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['email', 'password']
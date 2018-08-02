from django import forms

from .models import Profile

class UserCreationForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'email', 'password', 'birthdate']
		exclude = ['username', 'bio', 'avatar']


#class AuthenticationForm(forms.ModelForm):
#	class Meta:
#		model = Profile
#		fields = ['username', 'password']
#		exclude = ['firstname', 'lastname', 'email', 'birthdate',
#					'bio', 'avatar']
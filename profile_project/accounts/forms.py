from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
import re

from . import models

class CreateUserForm(UserCreationForm):
	'''Form for creating a new user.'''
	email_verification = forms.EmailField()
	class Meta:
		model = models.User
		fields = ['username', 'email', 'email_verification']
		
	# Checks to make sure that the given emails match.
	def clean(self):
		email = self.cleaned_data.get('email')
		ver_email = self.cleaned_data.get('email_verification')
		if email != ver_email:
			raise forms.ValidationError(
				'Whoops, it looks like your emails don\'t match'
			)
		return self.cleaned_data
		
class UpdateUserForm(forms.ModelForm):
	'''Form for updating the user form.'''
	class Meta:
		model = models.User
		fields = ['first_name', 'last_name', 'username', 'email']
		
class UpdateProfileForm(forms.ModelForm):
	'''Form for updating the profile form.'''
	class Meta:
		model = models.Profile
		fields = ['birthdate', 'bio', 'avatar']
		
	# Checks to make sure the length of the password
	# is greater than 10 characters long.
	def clean(self):
		bio = self.cleaned_data.get('bio')
		if len(bio) < 10 and len(bio) != 0:
			raise forms.ValidationError(
				'We want to know more about you! Your bio' +
				' needs to be at least ten characters long.'
			)
		return self.cleaned_data
		
class PasswordChangeForm(PasswordChangeForm):
	'''Form for changing the users password.'''
	class Meta:
		model = models.User
		fields = ['password1', 'password2']
		
	def clean(self):
		user = self.user
		old_password = self.cleaned_data.get('old_password')
		new_password = self.cleaned_data.get('new_password1')
		
		# Checks to make sure the old and new passwords don't match.
		if new_password == old_password:
			raise forms.ValidationError(
				'Your new password can\'t match your old password'
			)
			
		#https://stackoverflow.com/questions/17140408/if-statement-to-check-whether-a-string-has-a-capital-letter-a-lower-case-letter
		# Checks to make sure the new password contains capital letters.
		if not any(x.isupper() for x in new_password):
			raise forms.ValidationError(
				'Your new password must use capital letters'
			)
		
		# Checks to make sure the new password contains lower letters.
		if not any(x.islower() for x in new_password):
			raise forms.ValidationError(
				'Your new password must use lowercase letters'
			)
			
		if len(new_password) < 14:
			raise forms.ValidationError(
				'Your new password must be greater than 14 characters'
			)
			
		# Checks to make sure the new password contains digits.
		if not re.search('\d+', new_password):
			raise forms.ValidationError(
				'Your new password must contain one or more digits'
			)
			
		# Checks to make sure the new password contains special characters.
		if not re.search('[@#$]', new_password):
			raise forms.ValidationError(
				'Your new password must contain at least one special ' +
				'character, such as @, #, or $'
			)
			
		first_name = user.first_name.lower()
		last_name = user.last_name.lower()
		username = user.username.lower()
		
		# Checks to make sure the new password doesn't contain
		# the first name, last name, or username of the user.
		if (first_name or last_name or username) in new_password.lower():
			raise forms.ValidationError(
				'Your new password can\'t contain your first name, ' +
				'last name, or username'
			)
		
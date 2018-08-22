from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.utils.safestring import mark_safe
import re

from . import models

def check_password(password):
	if not any(x.isupper() for x in password):
		raise forms.ValidationError(
			'Your new password must use capital letters'
		)
	
	# Checks to make sure the new password contains lower letters.
	if not any(x.islower() for x in password):
		raise forms.ValidationError(
			'Your new password must use lowercase letters'
		)
		
	if len(password) < 14:
		raise forms.ValidationError(
			'Your new password must be greater than 14 characters'
		)
		
	# Checks to make sure the new password contains digits.
	if not re.search('\d+', password):
		raise forms.ValidationError(
			'Your new password must contain one or more digits'
		)
		
	# Checks to make sure the new password contains special characters.
	if not re.search('[@#$]', password):
		raise forms.ValidationError(
			'Your new password must contain at least one special ' +
			'character, such as @, #, or $'
		)

class CreateUserForm(UserCreationForm):
	'''Form for creating a new user.'''
	email_verification = forms.EmailField()
	password1 = forms.CharField(
				label="Password",
				widget=forms.PasswordInput,
				help_text=mark_safe(
				'<ul>'
				'<li>Your password must be at least 14 characters long</li>\n'
				'<li>Your password must use both upper and lowercase letters</li>\n'
				'<li>Your password must contain at least one digit</li>\n'
				'<li>Your password must contain at least one special '
				'character, such as @, #, or $</li>'
				'<li>Your password cannot contain your username</li>'
				'</ul>'
			))
	password2 = forms.CharField(
					label="Password Confirmation", widget=forms.PasswordInput,
					help_text='Enter the same password as above, for verification.'
				)
	class Meta:
		model = models.User
		fields = ['username', 'email', 'email_verification']
		
	# Checks to make sure that the given emails match.
	def clean(self):
		check_password(self.cleaned_data.get('password1'))
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
	password1 = forms.CharField(
				label="Password",
				widget=forms.PasswordInput,
				help_text=mark_safe(
				'<ul>'
				'<li>Your new password cannot be the same as your old password</li>\n'
				'<li>Your new password must be at least 14 characters long</li>\n'
				'<li>Your new password must use both upper and lowercase letters</li>\n'
				'<li>Your new password must contain at least one digit</li>\n'
				'<li>Your new password must contain at least one special '
				'character, such as @, #, or $</li>'
				'<li>Your new password cannot contain your username or parts of your '
				'first or last name</li>'
				'</ul>'
			))
	new_password1 = forms.CharField(label="New password confirmation",
									widget=forms.PasswordInput)
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
		
		check_password(new_password)
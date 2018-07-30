from django import forms

class UserCreationForm(forms.Form):
	firstname = forms.CharField()
	lastname = forms.CharField()
	email1 = forms.EmailField()
	email2 = forms.EmailField()
	password = forms.CharField()
	birthdate = forms.DateField()
	bio = forms.CharField(widget=forms.Textarea)
	avatar = forms.BooleanField(required=False)


class AuthenticationForm(forms.Form):
	email = forms.EmailField()
	password1 = forms.CharField()
	password2 = forms.CharField()

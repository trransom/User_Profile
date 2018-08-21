from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import pdb

from . import forms
from . import models

def sign_in(request):
    '''View for the sign-in page.'''
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile_view')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})

def sign_up(request):
    '''View for the sign-up page.'''
    form = forms.CreateUserForm()
    if request.method == 'POST':
        form = forms.CreateUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            profile = models.Profile(user=user)
            profile.save()
            if profile: print('profile created')
            return HttpResponseRedirect(reverse('accounts:profile_view'))# TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    '''View for the sign-out page.'''
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))
    
def profile_view(request):
    '''View to display the user's profile.'''
    user = request.user
    return render(request, 'accounts/display_profile.html', {'user': user})
    
def edit_profile(request):
	'''View to display the edit form.'''
	user = request.user
	user_form = forms.UpdateUserForm(instance=user)
	profile_form = forms.UpdateProfileForm(instance=user.profile)
	if request.method == 'POST':
		user_form = forms.UpdateUserForm(instance=user, data=request.POST)
		profile_form = forms.UpdateProfileForm(instance=user.profile, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return HttpResponseRedirect(reverse('accounts:profile_view'))
	return render(request, 'accounts/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
	
def change_password(request):
	'''View to display the form for changing passwords.'''
	form = forms.PasswordChangeForm(user=request.user)
	if request.method == 'POST':
		form = forms.PasswordChangeForm(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Your password was updated!')
			return HttpResponseRedirect(reverse('accounts:profile_view'))
	return render(request, 'accounts/password.html', {'form': form})
	
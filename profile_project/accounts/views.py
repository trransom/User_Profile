from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import pdb
from django.views.decorators.csrf import ensure_csrf_cookie

from . import forms
from . import models


def sign_in(request):
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

@ensure_csrf_cookie
def sign_up(request):
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
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))
    
def profile_view(request):
    user = request.user
    test = models.Profile.objects.get(id=1)
    print(test.bio)
    return render(request, 'accounts/display_profile.html', {'user': user})
	
def edit_profile(request):
	user = request.user
	user_form = forms.UpdateUserForm(instance=user)
	profile_form = forms.UpdateProfileForm(instance=user)
	if request.method == 'POST':
		user_form = forms.UpdateUserForm(instance=user, data=request.POST)
		profile_form = forms.UpdateProfileForm(instance=user.profile, data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return HttpResponseRedirect(reverse('accounts:profile_view'))
	return render(request, 'accounts/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

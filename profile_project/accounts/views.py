from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import pdb

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
                        reverse('profile_view')  # TODO: go to profile
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
    form = forms.CreateUserForm()
    if request.method == 'POST':
        form = forms.CreateUserForm(data=request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data['username'])
            print(form.cleaned_data['password1'])
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:profile_view'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


#def sign_up(request):
#    form = forms.UserCreationForm()
#    if request.method == 'POST':
#        form = forms.UserCreationForm(data=request.POST)
#        if form.is_valid():
#            form.save()
#            test = models.Profile.objects.get(first_name=form.cleaned_data['first_name'])
#            print(test.first_name)
#            print(test.last_name)
#            print(test.email)
#            print(test.password)
#            user = authenticate(
#                first_name=form.cleaned_data['first_name'],
#                last_name=form.cleaned_data['last_name'],
#                email=form.cleaned_data['email']
#            )
#            print(user)
#            login(request, user)
#            messages.success(
#                request,
#                "You're now a user! You've been signed in, too."
#            )
#            return HttpResponseRedirect(reverse('accounts:profile_view'))  # TODO: go to profile
#    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))
	
def profile_view(request, pk):
	user = get_object_or_404(models.User, pk=pk)
	return render(request, 'accounts/display_profile.html', {'user': user})

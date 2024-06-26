from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm, SignInForm
from django.db import Error
import hashlib

import data.database as db
import data.model as mod

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # is_valid function already checks if the user with this email already exists
            # or if the password and confirmed password are not the same 
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            password = form.cleaned_data['password']
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            user = mod.User(email=email, password=hashed_password, name=name, surname=surname)
            
            db.add_appuser(user) # Adds user to the database
            return redirect('home') # Redirect to user home page. For now this just redirects to global home page.
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            return redirect('home')    
    else:
        form = SignInForm()
    return render(request, 'users/sign-in.html', {'form': form})
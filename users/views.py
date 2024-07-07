from django.shortcuts import render, redirect
from .forms import RegistrationForm, SignInForm
import hashlib
from django.contrib import messages
from django.views.decorators.cache import cache_control

import data.database as db
import data.model as mod

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            password = form.cleaned_data['password']
            repeatPassword = form.cleaned_data['repeatPassword']

            # check if user with this email already exists
            if db.getUserByEmail(email) is not None:
                messages.error(request, 'Email already in use')
                return render(request, 'users/register.html', {'form': form})

            # check if password fields are the same
            if password and repeatPassword and password != repeatPassword:
                messages.error(request, 'Passwords do not match')
                return render(request, 'users/register.html', {'form': form})
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = mod.User(email=email, password=hashed_password, name=name, surname=surname)
            db.add_appuser(user) # Adds user to the database
            return redirect('home') # Redirect to user home page. For now this just redirects to home page.
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            user =  db.getUserByEmail(email) # gets user from database

            if user is None: 
                # User with this email does not exist
                messages.error(request, 'Email or password is incorrect')
                return render(request, 'users/sign-in.html', {'form': form})
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password != user.password: 
                # Incorrect password
                messages.error(request, 'Email or password is incorrect')
                return render(request, 'users/sign-in.html', {'form': form})
            
            # Store cookie session by user id
            request.session['user_id'] = user.id
            return redirect('profile')    
    else: # method GET
        if 'user_id' in request.session:
            # If user is already logged in redirects to his profile page
            return redirect('profile')

        form = SignInForm()
    return render(request, 'users/sign-in.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        print(user_id)
        return render(request, 'users/profile.html')
    else:
        return redirect('sign-in')
    
def sign_out(request):
    # Clear session
    del request.session['user_id']
    
    # Redirect to the home page
    return redirect('home')
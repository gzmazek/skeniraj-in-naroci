from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from django.db import connection
import hashlib

def home(request):
    return render(request, 'accounts/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO accounts_appuser (username, name, password, gender)
                    VALUES (%s, %s, %s, %s)
                """, [username, name, hashed_password, gender])
            
            return HttpResponse("User registered successfully")
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
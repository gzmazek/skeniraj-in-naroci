from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import SignInForm
from django.http import JsonResponse
from owners.forms import TableForm
import hashlib

from django.contrib import messages
from django.views.decorators.cache import cache_control
from owners.forms import AddRestaurantForm

import data.database as db
import data.model as mod

from owners.decorators import owner_required, restaurant_access_required

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True) # Prevents from browser caching page and hence rendering it when user is already logged out
@owner_required
def profile(request):
    owner_id = request.session['owner_id'][0]
    print(owner_id)
    if request.method == 'POST':
        form = AddRestaurantForm(request.POST)
        print("Request: POST")
        if form.is_valid():
            print("Valid form")
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            rest = db.addRestaurant(mod.Restaurant(name=name, location=address, owner_id=owner_id))

            # Update list of allowed restaurants
            list = request.session['owner_id'][1]
            list.append(rest.id)
            request.session['owner_id'] = (owner_id, list)
    else:
        form = AddRestaurantForm()

    restaurants = db.getRestaurantsOfOwner(owner_id)
    return render(request, 'owners/profile.html', {'restaurants': restaurants,'form': form})


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
                return render(request, 'owners/sign-in.html', {'form': form})
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password != user.password: 
                # Incorrect password
                messages.error(request, 'Email or password is incorrect')
                return render(request, 'owners/sign-in.html', {'form': form})
            
            restaurants = db.getRestaurantsOfOwner(user.id)
            allowed_restaurant_IDs = [] # List of all restaurant IDs owned by this user. Used later to check if user can access pages
            for rest in restaurants:
                allowed_restaurant_IDs.append(rest.id)

            # Store owner session by user id
            request.session['owner_id'] = (user.id, allowed_restaurant_IDs)
            return redirect('profile_rest')    
    else: # method GET
        if 'owner_id' in request.session:
            # If user is already logged in redirects to his profile page
            return redirect('profile_rest')

        form = SignInForm()
    return render(request, 'owners/sign-in.html', {'form': form})


def sign_out(request):
    # Clear session
    del request.session['owner_id']

    return redirect('profile_rest')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # Prevents from browser caching page and hence rendering it when user is already logged out
@restaurant_access_required
def restaurant_dashboard(request, unique_id: int):
    restaurant = db.getRestaurantByID(unique_id)
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'owners/dashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def restaurant_dashboard(request, unique_id: int):
    restaurant = db.getRestaurantByID(unique_id)
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'owners/dashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def tables_list(request, unique_id: int):
    restaurant = db.getRestaurantByID(unique_id)
    tables = db.getTablesByRestaurant(restaurant.id)
    context = {
        'restaurant': restaurant,
        'tables': tables,
    }
    return render(request, 'owners/tables_list.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def add_table(request, unique_id: int):
    try:
        restaurant = db.getRestaurantByID(unique_id)
        table = mod.Table(restaurant_id=restaurant.id)
        db.addTable(table)
        messages.success(request, 'Table added successfully.')
    except Exception as e:
        messages.error(request, f'Error adding table: {str(e)}')
    return redirect('tables_list', unique_id=unique_id)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def delete_table(request, unique_id: int, table_id: int):
    db.deleteTable(table_id)
    return redirect('tables_list', unique_id=unique_id)
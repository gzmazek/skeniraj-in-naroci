"""
VIEWS.PY - TABLE OF CONTENTS
============================

1. IMPORTS
--------------------------------
- Django imports (render, redirect, HttpResponse, etc.)
- Forms and Models
- Logging setup

2. HOME PAGE
--------------------------------
- home(request)

3. PROFILE VIEWS
--------------------------------
- profile(request)
- settings(request)

4. AUTHENTICATION VIEWS
--------------------------------
- sign_in(request)
- sign_out(request)
- register(request)

4. ORDER VIEWS
--------------------------------
- order(request, table_id: int)
- order_confirm(request)
- place_order(request)

5. QR SCANNING VIEWS
--------------------------------
- scan_qr(request)
- process_qr(request)

"""

from django.shortcuts import render, redirect
from .forms import RegistrationForm, SignInForm, ChangePasswordForm
import hashlib
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import data.database as db
import data.model as mod

import json

from users.decorators import user_sign_in_required, active_order


#########################################################
#                   HOME FUNCTIONS                      #
#########################################################
def home(request):
    """
    Home page of the website.
    """
    return render(request, 'users/home.html')

#########################################################
#                   PROFILE FUNCTIONS                      #
#########################################################
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_sign_in_required
def profile(request):
    """
    Profile page for users.
    """
    user_id = request.session['user_id']
    orders = db.getUserOrders(user_id)
    popularRestaurants = db.getUserPopularRestaurants(user_id)
    
    popularRestaurants_json = [rest.to_json(ensure_ascii=False) for rest in popularRestaurants]
    orders_json = [order.to_json(ensure_ascii=False) for order in orders]

    # Parse each JSON string into a JSON object
    orders = [json.loads(order) for order in orders_json]
    popularRestaurants = [json.loads(rest) for rest in popularRestaurants_json]
    
    return render(request, 'users/profile.html', {'orders': orders, 'popularRestaurants': popularRestaurants})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_sign_in_required
def settings(request):
    """
    Settings page for users.
    """
    if request.method == 'POST':
        user_id = request.session['user_id']
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            oldPass = form.cleaned_data['oldPass']
            newPass = form.cleaned_data['newPass']
            newPassRep = form.cleaned_data['newPassRep']

            hashed_password = hashlib.sha256(oldPass.encode()).hexdigest()
            user =  db.getUserByID(user_id) # gets user from database

            if user.password != hashed_password: 
                # old password is incorrect
                messages.error(request, 'Password is incorrect')
                return render(request, 'users/settings.html', {'form': form})
            
            if newPass != newPassRep: 
                # new password and repeated password are not equal
                messages.error(request, 'New password and repeated new password are not equal')
                return render(request, 'users/settings.html', {'form': form})
            
            hashed_password = hashlib.sha256(newPass.encode()).hexdigest()
            user = db.changeUserPassword(user_id, hashed_password)
            
            return redirect('settings')    
    else: # method GET
        form = ChangePasswordForm()
    return render(request, 'users/settings.html', {'form': form})

#########################################################
#              AUTHENTICATION FUNCTIONS                 #
#########################################################
def sign_in(request):
    """
    Sign-in page for users.
    """
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

@user_sign_in_required
def sign_out(request):
    """
    Sign-out and clear the session of the user.
    """
    # Clear session
    del request.session['user_id']
    
    # Redirect to the home page
    return redirect('home')

def register(request):
    """
    Register page to create new account. This account can be used both as a user or as a restaurant owner.
    """
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
            db.addAppuser(user) # Adds user to the database
            return redirect('home') # Redirect to user home page. For now this just redirects to home page.
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

#########################################################
#                  ORDER FUNCTIONS                      #
#########################################################
@user_sign_in_required
def order(request, table_id: int):
    """
    Page to order at a given table that belongs to some restaurant.
    """
    request.session['table_id'] = table_id

    restaurant = db.getRestaurantFromTableID(table_id)
    if restaurant == None:
        return render(request, 'users/table_not_exist.html')
    
    menu = db.getRestaurantMenu(restaurant.id)

    if request.method == 'POST':
        selected_items = []
        selected_item_quantities = []
        for item in menu:
            quantity = request.POST.get(f'quantity_{item.id}', 0)
            quantity = int(quantity)

            if quantity > 0:
                selected_items.append(item.to_dict())
                selected_item_quantities.append(quantity)

        request.session['selected_items'] = selected_items
        request.session['quantities'] = selected_item_quantities
        return redirect('order_confirm')

    return render(request, 'users/order.html', {'menu': menu, 'restaurant': restaurant, 'tableID': table_id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_sign_in_required
@active_order
def order_confirm(request):
    """
    Page to confirm the order.
    """
    selected_items = request.session['selected_items']
    quantities = request.session['quantities']

    total_price = 0
    for item, quantity in zip(selected_items, quantities):
        item['quantity'] = quantity
        item['price'] = "%.2f" % (quantity * item['value'])
        total_price += quantity * item['value']

    formatted_value = "%.2f" % total_price
    return render(request, 'users/order_confirm.html', {'items': selected_items, 'total_price': formatted_value})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_sign_in_required
@active_order
def place_order(request):
    """
    Function to place the order and add it to the database.
    """
    selected_items = request.session.pop('selected_items', {})
    quantities = request.session.pop('quantities', {})
    user_id = request.session['user_id']
    table_id = request.session['table_id']
    
    del request.session['table_id']

    order = db.addCustomerOrder(mod.CustomerOrder(user_id=user_id, table_id=table_id, status='IN PROGRESS'))

    for item, quantity in zip(selected_items, quantities):
        orderItem = mod.OrderItem(order_id=order.id, item_id=item['id'], quantity=quantity)
        db.addItemToOrder(orderItem)

    return redirect('profile')


#########################################################
#             QR CODE SCANNING FUNCTIONS                #
#########################################################
@user_sign_in_required
def scan_qr(request):
    """
    Page to scan QR code.
    """
    return render(request, 'users/qr_reader.html')

@csrf_exempt
def process_qr(request):
    """
    Function to process the QR code data and redirect accordingly.
    """
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')

        # Try to convert qr_data to an integer and check if it succeeds
        try:
            qr_data = int(qr_data)
            is_integer = True
        except ValueError:
            is_integer = False
        
        # Process the QR data based on its type
        if is_integer:
            # Logic for handling integer qr_data
            redirect_url = f'http://127.0.0.1:8000/order/{qr_data}/'  # IMPORTANT: This URL needs to be changed when app will be deplyed to some domain
        else:
            return JsonResponse({'message': 'Invalid QR code'}, status=400)

        response_data = {
            'redirect_url': redirect_url
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)









    
from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import SignInForm
from django.http import JsonResponse
import hashlib

from django.contrib import messages
from django.views.decorators.cache import cache_control
from owners.forms import AddRestaurantForm, AddItemForm

import data.database as db
import data.model as mod
from django.views.decorators.csrf import csrf_exempt
import json


from owners.decorators import owner_required, restaurant_access_required

import logging

logger = logging.getLogger(__name__)

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True) # Prevents from browser caching page and hence rendering it when user is already logged out
@owner_required
def profile(request):
    """
    Profile page of owner.
    """
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
    """
    Sign-in page for restaurants (owners)
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

@owner_required
def sign_out(request):
    """
    Sign-out function to terminate owner session
    """
    # Clear session
    del request.session['owner_id']

    return redirect('profile_rest')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def restaurant_dashboard(request, restaurant_id: int):
    """
    Main page for restaurant view. Displays tables and their orders.
    """
    restaurant = db.getRestaurantByID(restaurant_id)
    tables = db.getTablesByRestaurant(restaurant.id)

    table_orders_pairs = []
    for table in tables:
        orders = db.getOrdersByTableID(table.id)
        
        # Log the orders to ensure they're being fetched correctly
        print(f"Orders with items for table {table.id}: {orders}")

        table_orders_pairs.append(mod.TableOrders(table=table, orders=orders))

    tables_json = [table_orders_pair.to_json(ensure_ascii=False) for table_orders_pair in table_orders_pairs]
    tables = [json.loads(table) for table in tables_json]

    context = {
        'restaurant': restaurant,
        'tables': tables,
    }
    return render(request, 'owners/dashboard.html', context)

# Restaurant products view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def restaurant_products(request, unique_id: int):
    """
    Page where owners can add or remove items from the restaurant menu
    """
    restaurant = db.getRestaurantByID(unique_id)
    
    menu = db.getRestaurantMenu(restaurant.id)

    menu_json = [item.to_json(ensure_ascii=False) for item in menu]
    # Parse each JSON string into a JSON object
    menu = [json.loads(item) for item in menu_json]

    context = {
        'restaurant': restaurant,
        'menu': menu,
    }
    return render(request, 'owners/products.html', context)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def save_table_position(request, restaurant_id, table_id):
    """
    Function to save table position to the database.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        position_x = data.get('x', 0)
        position_y = data.get('y', 0)
        logger.debug(f"Received table_id: {table_id}, position_x: {position_x}, position_y: {position_y}")
        try:
            db.updateTablePosition(int(table_id), int(position_x), int(position_y))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error updating table position: {e}")
            return JsonResponse({'status': 'failed', 'error': str(e)})
    return JsonResponse({'status': 'failed'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def add_table(request, restaurant_id: int):
    """
    Function to add new table for a restaurant and saves it to the database.
    """
    if request.method == 'POST':
        restaurant = db.getRestaurantByID(restaurant_id)
        table = mod.Table(restaurant_id=restaurant.id, position_x=0, position_y=0)
        db.addTable(table)
        return JsonResponse({'status': 'success', 'table_id': table.id})
    return JsonResponse({'status': 'failed'})

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@restaurant_access_required
def delete_table(request, restaurant_id: int, table_id: int):
    """
    Function to delete table from the restaurant and database.
    """
    if request.method == 'POST':
        table = db.getTableByID(table_id)
        # check if table belongs to this restaurant
        if table.restaurant_id == restaurant_id:
            db.deleteTable(table_id) # delete table
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def customers_view(request):
    context = {}
    return render(request, 'owners/customers.html', context)

@restaurant_access_required
def mark_item_prepared(request, restaurant_id:int, item_id:int, order_id:int):
    """
    Function to mark item from customer order as prepared. When all items in order are prepared
    the order can be delivered.
    """
    if request.method == "POST":
        success = db.markItemAsPrepared(item_id, order_id)
        return JsonResponse({'success': success})
    return JsonResponse({'success': False}, status=400)

@restaurant_access_required
def mark_order_prepared(request, restaurant_id:int, order_id:int):
    """
    Function to mark all elements in customer order as prepared. After it the order can be delivered.
    """
    if request.method == "POST":
        orderItems = db.getItemsByOrderID(order_id)
        success = True
        for item in orderItems:
            success = db.markItemAsPrepared(item.item_id, order_id) and success
        return JsonResponse({'success': success})
    return JsonResponse({'success': False}, status=400)

@restaurant_access_required
def mark_order_delivered(request, restaurant_id:int, order_id:int):
    """
    Function to mark order as delivered. This is a final step of customer order after which the order is labeled as FINISHED.
    """
    if request.method == "POST":
        success = db.markOrderAsDelivered(order_id)
        return JsonResponse({'success': success})
    return JsonResponse({'success': False}, status=400)

@restaurant_access_required
def get_items_by_order_id(request, restaurant_id, order_id):
    """
    Function to get all items for the given order.
    """
    if request.method == "GET":
        items = db.getItemsByOrderID(order_id) 
        items_data = [
            {
                'name': db.getItemNameByID(item.item_id),
                'item_id': item.item_id,
                'quantity': item.quantity,
                'status': item.status
            } for item in items
        ]
        return JsonResponse({'items': items_data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@restaurant_access_required
def remove_menu_items(request, restaurant_id):
    """
    Function to remove the item from restaurant menu. It does not remove the item from database, just its relation to the restaurant menu.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        success = True
        for i in data:
            success = db.removeItemFromRestaurantMenu(i, restaurant_id) and success
        return JsonResponse({'success': success})
    return JsonResponse({'success': False})

@restaurant_access_required
def add_menu_item(request, restaurant_id):
    """
    Function to add a new item to restaurant menu. First the new item is created and added to the database, then it is mapped to restaurant menu
    to indicate that this item belongs on the menu.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data["name"]
        value = data["value"]

        item = db.addNewItem(mod.Item(name=name, value=value))
        success = db.addItemToRestaurantMenu(restaurant_id, item)
        return JsonResponse({'success': success})
    return JsonResponse({'success': False})
        

from data.model import Restaurant
from django.http import Http404

@restaurant_access_required
def settings_view(request, restaurant_id):
    """
    Settings page for owner profile.
    """
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        raise Http404("Restaurant does not exist")

    context = {
        'restaurant': restaurant,
    }
    return render(request, 'owners/settings.html', context)

import qrcode
from io import BytesIO

def generate_qr_code(request, table_id):
    """
    Page with the QR code for given table, so that users can scan it and order.
    """
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR Code, higher value means bigger size
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # controls the error correction used for the QR Code
        box_size=20,  # size of each box in pixels
        border=4,  # thickness of the border (in boxes)
    )

    # Add data to the QR code
    qr.add_data(table_id)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image in a BytesIO object
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    # Return the image as an HTTP response
    return HttpResponse(img_io, content_type='image/png')

def revive_order(request, restaurant_id, table_id):
    try:
        # Find the last finished order by table_id
        last_finished_order = db.get_last_finished_order_by_table_id(table_id)
        
        if last_finished_order is not None:
            # Reset the status of the last finished order
            db.update_order_status(last_finished_order['id'], 'IN PROGRESS')

            # Reset the status of all items in the order
            db.update_order_items_status(last_finished_order['id'], 'pending')

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'No finished order found for this table.'})
    except Exception as e:
        print(f"Error reviving order: {e}")
        return JsonResponse({'success': False, 'error': str(e)})

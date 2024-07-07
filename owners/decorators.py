from django.shortcuts import render, redirect

# Decorator to check if owner_id is in session
def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'owner_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('sign-in_rest')
    return wrapper

# Decorator to check if unique_id is in request.session['owner_id'][1] aka. owner can acess this restaurant
# Also checks if owner_id is in session
def restaurant_access_required(view_func):
    def wrapper(request, unique_id, *args, **kwargs):
        if 'owner_id' in request.session and unique_id in request.session['owner_id'][1]:
            return view_func(request, unique_id, *args, **kwargs)
        else:
            return redirect('profile_rest')
    return wrapper
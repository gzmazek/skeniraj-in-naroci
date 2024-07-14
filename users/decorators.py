from django.shortcuts import render, redirect

# Decorator to check if owner_id is in session
def user_sign_in_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('sign-in')
    return wrapper
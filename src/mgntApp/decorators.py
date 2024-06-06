from django.http import HttpResponse
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else: 
            return view_func(request, *args, **kwargs)

    return wrapper_func


# a decorator is a func that takes in another func in as a parameter 
# and lets us add extra functionality beforre the original functio is called

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
            # print(allowed_roles)
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group =  None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            # print(group)

        if group == 'customer':
            # print('yes')
            return HttpResponseRedirect(reverse('user_page'))
        
        if group == 'admin':
            # print('done')
            return view_func(request, *args, **kwargs)
        
        # return HttpResponseRedirect(reverse('user_page'))
          
    return wrapper_function

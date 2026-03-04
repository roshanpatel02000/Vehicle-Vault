from django.shortcuts import redirect,reverse,HttpResponse
from django.contrib import messages


def role_required(allowed_roles=[]):
    def decorator(view_func): # ownerDashboardView
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")  #urls.py name
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)   
            else:
                messages.error(request, "You are not authorized to view this page.")
                if request.user.role == "Admin":
                    return redirect("admin_dashboard")
                else:
                    return redirect("user_dashboard")
        return wrapper_func                      
    return decorator    

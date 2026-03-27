from django.shortcuts import render, redirect, get_object_or_404
from .models import Accessory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from vehicle.decorators import role_required
from .forms import AccessoryForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def accessoryListView(request):
    accessories = Accessory.objects.filter(availability=True)

    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        accessories = accessories.filter(
            Q(accessory_name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(vehicle_type__icontains=search_query)
        )

    # Filtering functionality
    category_filter = request.GET.get('category', '')
    if category_filter:
        accessories = accessories.filter(vehicle_type__icontains=category_filter)
        
    brand_filter = request.GET.get('brand', '')
    if brand_filter:
        accessories = accessories.filter(brand__icontains=brand_filter)

    # Get distinct categories and brands for the filter sidebar
    categories = Accessory.objects.filter(availability=True).values_list('vehicle_type', flat=True).distinct()
    # Handle potentially null/empty brands
    brands = Accessory.objects.filter(availability=True).exclude(brand__isnull=True).exclude(brand__exact='').values_list('brand', flat=True).distinct()

    context = {
        'accessories': accessories,
        'search_query': search_query,
        'category_filter': category_filter,
        'brand_filter': brand_filter,
        'categories': [c for c in categories if c], # clean up empty strings just in case
        'brands': brands,
    }
    
    # Pass favourited accessory IDs if user is logged in
    if request.user.is_authenticated:
        from .models import FavouriteAccessory
        favourite_ids = FavouriteAccessory.objects.filter(user=request.user).values_list('accessory_id', flat=True)
        context['favourite_accessory_ids'] = list(favourite_ids)
    
    return render(request, 'accessories.html', context)

# --- User Views ---

@login_required(login_url="login")
@require_POST
def toggle_favourite_accessory(request, accessory_id):
    """Toggle favourite status of an accessory for the logged-in user."""
    from .models import FavouriteAccessory
    
    accessory = get_object_or_404(Accessory, id=accessory_id)
    favourite, created = FavouriteAccessory.objects.get_or_create(
        user=request.user,
        accessory=accessory
    )
    
    if not created:
        favourite.delete()
        return JsonResponse({'status': 'removed'})
    
    return JsonResponse({'status': 'saved'})

@login_required(login_url="login")
def favouriteAccessoriesView(request):
    """Display the accessories favourited by the user."""
    from .models import FavouriteAccessory
    
    favourite_objs = FavouriteAccessory.objects.filter(user=request.user).select_related('accessory').order_by('-created_at')
    favourite_accessories = [obj.accessory for obj in favourite_objs]
    
    # Also pass favourite_accessory_ids so the heart icon can be rendered as active
    favourite_accessory_ids = [a.id for a in favourite_accessories]
    
    return render(request, 'accessory/user/favourite_accessories.html', {
        'favourite_accessories': favourite_accessories,
        'favourite_accessory_ids': favourite_accessory_ids,
    })

# --- Admin Views ---

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def admin_manage_accessories(request):
    query = request.GET.get('q', '').strip()
    accessories = Accessory.objects.all()
    
    if query:
        accessories = accessories.filter(
            Q(accessory_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(vehicle_type__icontains=query)
        )
        
    accessories = accessories.order_by('-id')
    return render(request, "accessory/admin/manage_accessories.html", {
        'accessories': accessories,
        'search_query': query
    })

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def admin_add_accessory(request):
    if request.method == "POST":
        form = AccessoryForm(request.POST, request.FILES)
        if form.is_valid():
            accessory = form.save()
            messages.success(request, f"Accessory '{accessory.accessory_name}' added successfully.")
            return redirect('admin_manage_accessories')
    else:
        form = AccessoryForm()
    
    return render(request, "accessory/admin/add_edit_accessory.html", {'form': form, 'title': 'Add Accessory'})

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def admin_edit_accessory(request, accessory_id):
    accessory = get_object_or_404(Accessory, id=accessory_id)
    
    if request.method == "POST":
        form = AccessoryForm(request.POST, request.FILES, instance=accessory)
        if form.is_valid():
            form.save()
            messages.success(request, f"Accessory '{accessory.accessory_name}' updated successfully.")
            return redirect('admin_manage_accessories')
    else:
        form = AccessoryForm(instance=accessory)
        
    return render(request, "accessory/admin/add_edit_accessory.html", {
        'form': form, 
        'accessory': accessory,
        'title': 'Edit Accessory'
    })

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def admin_delete_accessory(request, accessory_id):
    if request.method == "POST":
        accessory = get_object_or_404(Accessory, id=accessory_id)
        name = accessory.accessory_name
        accessory.delete()
        messages.success(request, f"Accessory '{name}' has been permanently deleted.")
    
    return redirect('admin_manage_accessories')

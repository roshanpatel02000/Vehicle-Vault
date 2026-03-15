from django.shortcuts import render, redirect, get_object_or_404
from .models import Accessory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from vehicle.decorators import role_required
from .forms import AccessoryForm
from django.contrib import messages

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
    return render(request, 'accessories.html', context)

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

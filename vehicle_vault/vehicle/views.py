from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Q
from decimal import Decimal
import json

from .decorators import role_required
from .models import Vehicle, VehicleComparison
from accessory.models import Accessory, VehicleAccessoryMap


def _run_comparison(v1, v2):
    """Core comparison logic shared by page view and AJAX view."""
    def cat_match(a, b):
        return 1 if str(a).lower() == str(b).lower() else 0

    def numeric_closeness(a, b):
        a, b = float(a), float(b)
        mx = max(abs(a), abs(b))
        return 1.0 if mx == 0 else 1.0 - abs(a - b) / mx

    score_points, total_points = 0, 0
    for pair in [(v1.fuel_type, v2.fuel_type), (v1.transmission, v2.transmission), (v1.body_type or '', v2.body_type or '')]:
        score_points += cat_match(*pair); total_points += 1
    for a, b in [(v1.price, v2.price), (v1.mileage, v2.mileage), (v1.seating_capacity, v2.seating_capacity)]:
        score_points += numeric_closeness(a, b); total_points += 1
    similarity_score = round((score_points / total_points) * 100, 2)

    def vehicle_score(v):
        price_val   = float(v.offer_price if v.offer_price else v.price)
        price_score = max(0, 1 - price_val / 10_000_000)
        mil         = float(v.mileage)
        mileage_score = (mil / 40.0) if mil > 0 else 0.5
        disc_score  = (float(v.discount_percentage) / 100.0) if v.discount_percentage else 0.0
        seat_score  = min(float(v.seating_capacity) / 8.0, 1.0)
        return 0.30 * mileage_score + 0.25 * price_score + 0.20 * disc_score + 0.15 * seat_score

    s1, s2 = vehicle_score(v1), vehicle_score(v2)
    if abs(s1 - s2) < 0.02:
        best_name, best_id = "Both vehicles are evenly matched", None
    elif s1 > s2:
        best_name, best_id = f"{v1.brand} {v1.model}", v1.pk
    else:
        best_name, best_id = f"{v2.brand} {v2.model}", v2.pk

    def field_winner(val1, val2, higher_is_better=True):
        try:
            f1, f2 = float(str(val1)), float(str(val2))
            if f1 == f2: return 'tie'
            return 'v1' if (f1 > f2) == higher_is_better else 'v2'
        except (ValueError, TypeError):
            return 'tie'

    comparison_fields = [
        {'label': 'Price (₹)',      'v1': str(v1.price),  'v2': str(v2.price),  'winner': field_winner(v1.price, v2.price, False), 'note': 'Lower is better'},
        {'label': 'Offer Price (₹)','v1': str(v1.offer_price) if v1.offer_price else '—', 'v2': str(v2.offer_price) if v2.offer_price else '—', 'winner': field_winner(v1.offer_price or v1.price, v2.offer_price or v2.price, False), 'note': 'Lower is better'},
        {'label': 'Discount',       'v1': f"{v1.discount_percentage}%" if v1.discount_percentage else '—', 'v2': f"{v2.discount_percentage}%" if v2.discount_percentage else '—', 'winner': field_winner(v1.discount_percentage or 0, v2.discount_percentage or 0), 'note': 'Higher is better'},
        {'label': 'Fuel Type',      'v1': v1.fuel_type,   'v2': v2.fuel_type,   'winner': 'tie', 'note': ''},
        {'label': 'Transmission',   'v1': v1.transmission,'v2': v2.transmission,'winner': 'tie', 'note': ''},
        {'label': 'Engine',         'v1': v1.engine,      'v2': v2.engine,      'winner': 'tie', 'note': ''},
        {'label': 'Mileage (km/l)', 'v1': str(v1.mileage) if float(v1.mileage) > 0 else 'EV', 'v2': str(v2.mileage) if float(v2.mileage) > 0 else 'EV', 'winner': field_winner(v1.mileage, v2.mileage), 'note': 'Higher is better'},
        {'label': 'Seating',        'v1': str(v1.seating_capacity), 'v2': str(v2.seating_capacity), 'winner': field_winner(v1.seating_capacity, v2.seating_capacity), 'note': 'Higher is better'},
        {'label': 'Body Type',      'v1': v1.body_type or '—', 'v2': v2.body_type or '—', 'winner': 'tie', 'note': ''},
    ]
    return similarity_score, best_name, best_id, comparison_fields


# ──────────────────────────────────────────────────────────────────────────────
def homeView(request):
    featured_vehicles = Vehicle.objects.filter(is_featured=True).order_by('-created_at')
    most_searched_vehicles = Vehicle.objects.all().order_by('-search_count')
    all_vehicles      = Vehicle.objects.all().order_by('brand', 'model')
    vehicle_count     = Vehicle.objects.count()
    return render(request, "home.html", {
        'featured_vehicles': featured_vehicles,
        'most_searched_vehicles': most_searched_vehicles,
        'all_vehicles': all_vehicles,
        'vehicle_count': vehicle_count,
    })


# ──────────────────────────────────────────────────────────────────────────────
def allVehiclesView(request):
    """Browse all vehicles page with optional filters."""
    from django.db.models import Q

    q          = request.GET.get('q', '').strip()
    fuel_type  = request.GET.get('fuel', '').strip()
    body_type  = request.GET.get('body', '').strip()

    vehicles = Vehicle.objects.all()

    if q:
        vehicles = vehicles.filter(
            Q(brand__icontains=q) |
            Q(model__icontains=q) |
            Q(variant__icontains=q)
        )
        # Increment search count for vehicles in results
        vehicles.update(search_count=F('search_count') + 1)

    if fuel_type:
        vehicles = vehicles.filter(fuel_type__iexact=fuel_type)

    if body_type:
        vehicles = vehicles.filter(body_type__iexact=body_type)

    vehicles = vehicles.order_by('-is_featured', 'brand', 'model')

    fuel_choices = Vehicle.FUEL_CHOICES
    body_choices = Vehicle.BODY_CHOICES

    return render(request, "vehicle/all_vehicles.html", {
        'vehicles': vehicles,
        'vehicle_count': vehicles.count(),
        'fuel_choices': fuel_choices,
        'body_choices': body_choices,
        'selected_fuel': fuel_type,
        'selected_body': body_type,
        'search_query': q,
    })


# ──────────────────────────────────────────────────────────────────────────────
def searchVehiclesView(request):
    """AJAX search endpoint: GET /search/?q=&fuel_type=&min_price=&max_price="""
    from django.db.models import Q

    q          = request.GET.get('q', '').strip()
    fuel_type  = request.GET.get('fuel_type', '').strip()
    min_price  = request.GET.get('min_price', '').strip()
    max_price  = request.GET.get('max_price', '').strip()

    vehicles = Vehicle.objects.all()

    if q:
        vehicles = vehicles.filter(
            Q(brand__icontains=q) |
            Q(model__icontains=q) |
            Q(variant__icontains=q) |
            Q(fuel_type__icontains=q)
        )

    if fuel_type:
        vehicles = vehicles.filter(fuel_type__iexact=fuel_type)

    try:
        if min_price:
            vehicles = vehicles.filter(price__gte=Decimal(min_price))
        if max_price:
            vehicles = vehicles.filter(price__lte=Decimal(max_price))
    except Exception:
        pass

    vehicles = vehicles.order_by('-is_featured', 'brand', 'model')[:8]

    results = []
    for v in vehicles:
        results.append({
            'id':          v.pk,
            'brand':       v.brand,
            'model':       v.model,
            'variant':     v.variant or '',
            'price':       str(v.price),
            'offer_price': str(v.offer_price) if v.offer_price else None,
            'fuel_type':   v.fuel_type,
            'body_type':   v.body_type or '',
            'image':       v.get_display_image(),
            'is_featured': v.is_featured,
        })

    return JsonResponse({'results': results, 'count': len(results)})


# ──────────────────────────────────────────────────────────────────────────────
def vehicleDetailView(request, vehicle_id):
    """JSON endpoint: GET /vehicle/<id>/detail/ — returns full vehicle specs."""
    try:
        v = Vehicle.objects.get(pk=vehicle_id)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found.'}, status=404)

    data = {
        'id':                  v.pk,
        'brand':               v.brand,
        'model':               v.model,
        'variant':             v.variant or '',
        'price':               str(v.price),
        'offer_price':         str(v.offer_price) if v.offer_price else None,
        'discount_percentage': v.discount_percentage,
        'fuel_type':           v.fuel_type,
        'transmission':        v.transmission,
        'engine':              v.engine,
        'mileage':             str(v.mileage),
        'seating_capacity':    v.seating_capacity,
        'body_type':           v.body_type or '',
        'color':               v.color or '',
        'description':         v.description or '',
        'image':               v.get_display_image(),
        'is_featured':         v.is_featured,
        'accessories': [
            {
                'name': mapping.accessory.accessory_name,
                'price': str(mapping.accessory.price),
                'brand': mapping.accessory.brand or 'N/A',
                'description': mapping.accessory.description or '',
                'image': mapping.accessory.image.url if mapping.accessory.image else '',
            }
            for mapping in v.accessory_mappings.all()
        ]
    }
    return JsonResponse(data)


# ──────────────────────────────────────────────────────────────────────────────
def comparisonPageView(request):
    """Dedicated comparison page: GET /compare/?v1=ID&v2=ID"""
    v1_id = request.GET.get('v1')
    v2_id = request.GET.get('v2')
    all_vehicles = Vehicle.objects.all().order_by('brand', 'model')

    error = None
    context = {'all_vehicles': all_vehicles}

    if v1_id and v2_id:
        if v1_id == v2_id:
            error = 'Please select two different vehicles.'
        else:
            try:
                v1 = Vehicle.objects.get(pk=v1_id)
                v2 = Vehicle.objects.get(pk=v2_id)
                similarity_score, best_name, best_id, comparison_fields = _run_comparison(v1, v2)

                user = request.user if request.user.is_authenticated else None
                VehicleComparison.objects.create(
                    vehicle1=v1, vehicle2=v2,
                    compared_by=user,
                    similarity_score=Decimal(str(similarity_score)),
                    best_vehicle=best_name,
                )
                context.update({
                    'v1': v1, 'v2': v2,
                    'similarity_score': similarity_score,
                    'best_name': best_name,
                    'best_id': best_id,
                    'comparison_fields': comparison_fields,
                    'v1_selected': v1_id,
                    'v2_selected': v2_id,
                })
            except Vehicle.DoesNotExist:
                error = 'One or both vehicles not found.'

    if error:
        context['error'] = error
    return render(request, 'comparison/comparison.html', context)


# ──────────────────────────────────────────────────────────────────────────────
@require_POST
@csrf_exempt
def compareVehiclesView(request):
    """AJAX endpoint: compare two vehicles, return JSON result."""
    try:
        data = json.loads(request.body)
        v1_id = int(data.get('vehicle1_id', 0))
        v2_id = int(data.get('vehicle2_id', 0))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid request.'}, status=400)

    if v1_id == v2_id:
        return JsonResponse({'error': 'Please select two different vehicles.'}, status=400)

    try:
        v1 = Vehicle.objects.get(pk=v1_id)
        v2 = Vehicle.objects.get(pk=v2_id)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found.'}, status=404)

    # ── Similarity score ───────────────────────────────────────────────────────
    # Categorical matches (each worth 1 point)
    score_points = 0
    total_points = 0

    def cat_match(a, b):
        return 1 if str(a).lower() == str(b).lower() else 0

    def numeric_closeness(a, b):
        """Return 0–1 similarity; 1 = equal."""
        a, b = float(a), float(b)
        if a == 0 and b == 0:
            return 1.0
        mx = max(abs(a), abs(b))
        if mx == 0:
            return 1.0
        return 1.0 - abs(a - b) / mx

    # Categorical (fuel, transmission, body_type)
    for field_pair in [
        (v1.fuel_type, v2.fuel_type),
        (v1.transmission, v2.transmission),
        (v1.body_type or '', v2.body_type or ''),
    ]:
        score_points += cat_match(*field_pair)
        total_points += 1

    # Numeric (price, mileage, seating_capacity)
    for a, b in [
        (v1.price, v2.price),
        (v1.mileage, v2.mileage),
        (v1.seating_capacity, v2.seating_capacity),
    ]:
        score_points += numeric_closeness(a, b)
        total_points += 1

    similarity_score = round((score_points / total_points) * 100, 2)

    # ── Best vehicle score (weighted) ─────────────────────────────────────────
    def vehicle_score(v):
        # Lower price → better (normalised against max possible = 10M)
        price_val = float(v.offer_price if v.offer_price else v.price)
        price_score = max(0, 1 - price_val / 10_000_000)

        # Higher mileage → better (EV mileage 0 gets neutral 0.5)
        mil = float(v.mileage)
        mileage_score = (mil / 40.0) if mil > 0 else 0.5

        # Discount
        disc_score = (float(v.discount_percentage) / 100.0) if v.discount_percentage else 0.0

        # Seating
        seat_score = min(float(v.seating_capacity) / 8.0, 1.0)

        return (
            0.30 * mileage_score +
            0.25 * price_score +
            0.20 * disc_score +
            0.15 * seat_score
        )

    s1 = vehicle_score(v1)
    s2 = vehicle_score(v2)

    if abs(s1 - s2) < 0.02:
        best_name = "Both vehicles are evenly matched"
        best_id   = None
    elif s1 > s2:
        best_name = f"{v1.brand} {v1.model}"
        best_id   = v1.pk
    else:
        best_name = f"{v2.brand} {v2.model}"
        best_id   = v2.pk

    # ── Persist comparison ────────────────────────────────────────────────────
    user = request.user if request.user.is_authenticated else None
    VehicleComparison.objects.create(
        vehicle1=v1,
        vehicle2=v2,
        compared_by=user,
        similarity_score=Decimal(str(similarity_score)),
        best_vehicle=best_name,
    )

    # ── Field-level comparison for the UI table ───────────────────────────────
    def field_winner(val1, val2, higher_is_better=True):
        """Return 'v1', 'v2', or 'tie'."""
        try:
            f1, f2 = float(str(val1)), float(str(val2))
            if f1 == f2:
                return 'tie'
            return 'v1' if (f1 > f2) == higher_is_better else 'v2'
        except (ValueError, TypeError):
            return 'tie' if str(val1) == str(val2) else 'tie'

    comparison_fields = [
        {
            'label': 'Price (₹)',
            'v1': str(v1.price),
            'v2': str(v2.price),
            'winner': field_winner(v1.price, v2.price, higher_is_better=False),
            'note': 'Lower is better',
        },
        {
            'label': 'Offer Price (₹)',
            'v1': str(v1.offer_price) if v1.offer_price else '—',
            'v2': str(v2.offer_price) if v2.offer_price else '—',
            'winner': field_winner(
                v1.offer_price or v1.price,
                v2.offer_price or v2.price,
                higher_is_better=False,
            ),
            'note': 'Lower is better',
        },
        {
            'label': 'Discount',
            'v1': f"{v1.discount_percentage}%" if v1.discount_percentage else '—',
            'v2': f"{v2.discount_percentage}%" if v2.discount_percentage else '—',
            'winner': field_winner(v1.discount_percentage or 0, v2.discount_percentage or 0),
            'note': 'Higher is better',
        },
        {
            'label': 'Fuel Type',
            'v1': v1.fuel_type,
            'v2': v2.fuel_type,
            'winner': 'tie',
            'note': '',
        },
        {
            'label': 'Transmission',
            'v1': v1.transmission,
            'v2': v2.transmission,
            'winner': 'tie',
            'note': '',
        },
        {
            'label': 'Engine',
            'v1': v1.engine,
            'v2': v2.engine,
            'winner': 'tie',
            'note': '',
        },
        {
            'label': 'Mileage (km/l)',
            'v1': str(v1.mileage) if float(v1.mileage) > 0 else 'EV',
            'v2': str(v2.mileage) if float(v2.mileage) > 0 else 'EV',
            'winner': field_winner(v1.mileage, v2.mileage),
            'note': 'Higher is better',
        },
        {
            'label': 'Seating',
            'v1': str(v1.seating_capacity),
            'v2': str(v2.seating_capacity),
            'winner': field_winner(v1.seating_capacity, v2.seating_capacity),
            'note': 'Higher is better',
        },
        {
            'label': 'Body Type',
            'v1': v1.body_type or '—',
            'v2': v2.body_type or '—',
            'winner': 'tie',
            'note': '',
        },
    ]

    return JsonResponse({
        'vehicle1': v1.to_dict(),
        'vehicle2': v2.to_dict(),
        'similarity_score': similarity_score,
        'best_vehicle': best_name,
        'best_id': best_id,
        'comparison_fields': comparison_fields,
    })


@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def AdminDashboardView(request):
    from core.models import User
    from Notification.models import Notification
    from accessory.models import Accessory
    
    total_users = User.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_notifications = Notification.objects.count()
    total_accessories = Accessory.objects.count()
    
    context = {
        'total_users': total_users,
        'total_vehicles': total_vehicles,
        'total_notifications': total_notifications,
        'total_accessories': total_accessories
    }
    return render(request, "vehicle/admin/Admin_dashboard.html", context)


@login_required(login_url="login")
@role_required(allowed_roles=["User"])
def UserDashboardView(request):
    from Notification.models import UserNotification
    unread_notifications = UserNotification.objects.filter(user=request.user, is_read=False).count()
    return render(request, "vehicle/user/User_dashboard.html", {
        'total_notifications': unread_notifications
    })

# ─── Admin Approvals ────────────────────────────────────────────────────────
@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def PendingAdminsView(request):
    from core.models import User
    pending_admins = User.objects.filter(role='Admin', is_approved=False).order_by('-created_at')
    return render(request, "vehicle/admin/pending_admins.html", {'pending_admins': pending_admins})

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def ManageUsersView(request):
    from core.models import User
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    users = User.objects.all()
    
    if query:
        users = users.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(role__icontains=query)
        )
        
    users = users.order_by('-created_at')
    return render(request, "vehicle/admin/manage_users.html", {'users': users, 'search_query': query})

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def DeleteUserView(request, user_id):
    from core.models import User
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    
    if request.method == "POST":
        user_to_delete = get_object_or_404(User, id=user_id)
        
        # Prevent an admin from deleting their own account
        if user_to_delete == request.user:
            messages.error(request, "You cannot delete your own admin account.")
        else:
            name = f"{user_to_delete.first_name} {user_to_delete.last_name}" if user_to_delete.first_name else user_to_delete.email
            user_to_delete.delete()
            messages.success(request, f"User '{name}' has been permanently deleted.")
            
    return redirect('manage_users')

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def ManageVehiclesView(request):
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    vehicles = Vehicle.objects.all()
    
    if query:
        vehicles = vehicles.filter(
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(variant__icontains=query) |
            Q(fuel_type__icontains=query) |
            Q(transmission__icontains=query) |
            Q(body_type__icontains=query)
        )
        
    vehicles = vehicles.order_by('-created_at')
    return render(request, "vehicle/admin/manage_vehicles.html", {'vehicles': vehicles, 'search_query': query})

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def AddVehicleView(request):
    from .forms import VehicleForm
    from django.contrib import messages
    
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f"Vehicle '{vehicle.brand} {vehicle.model}' added successfully.")
            return redirect('manage_vehicles')
    else:
        form = VehicleForm()
    
    return render(request, "vehicle/admin/add_vehicle.html", {'form': form})

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def DeleteVehicleView(request, vehicle_id):
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    
    if request.method == "POST":
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        name = f"{vehicle.brand} {vehicle.model}"
        vehicle.delete()
        messages.success(request, f"Vehicle '{name}' has been permanently deleted.")
    
    return redirect('manage_vehicles')

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def EditVehicleView(request, vehicle_id):
    from .forms import VehicleForm
    from django.shortcuts import get_object_or_404
    from django.contrib import messages

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vehicle '{vehicle.brand} {vehicle.model}' updated successfully.")
            return redirect('manage_vehicles')
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, "vehicle/admin/edit_vehicle.html", {'form': form, 'vehicle': vehicle})

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def ApproveAdminView(request, user_id):
    from core.models import User
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    
    admin_to_approve = get_object_or_404(User, id=user_id, role='Admin', is_approved=False)
    admin_to_approve.is_approved = True
    admin_to_approve.save()
    
    messages.success(request, f"Admin account for {admin_to_approve.email} has been approved.")
    return redirect('pending_admins')


# ─── Static Content Pages ────────────────────────────────────────────────────
def aboutView(request):
    """Render the About Us page."""
    return render(request, "about.html")


def servicesView(request):
    """Render the Services page."""
    return render(request, "services.html")

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def RejectAdminView(request, user_id):
    from core.models import User
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    
    admin_to_reject = get_object_or_404(User, id=user_id, role='Admin', is_approved=False)
    email = admin_to_reject.email
    admin_to_reject.delete()
    
    messages.success(request, f"Review dismissed. The pending request for {email} has been rejected and deleted.")
    return redirect('pending_admins')
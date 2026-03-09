from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from vehicle.decorators import role_required
from .models import Notification, UserNotification
from .forms import NotificationForm

@login_required
def fetch_notifications(request):
    """Fetch recent notifications for the dropdown."""
    notifications = UserNotification.objects.filter(
        user=request.user, 
        notification__is_active=True
    ).order_by('-notification__created_at')[:5]
    
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'title': n.notification.title,
            'message': n.notification.message[:100] + ('...' if len(n.notification.message) > 100 else ''),
            'created_at': n.notification.created_at.strftime('%Y-%m-%d %H:%M'),
            'is_read': n.is_read
        })
    
    return JsonResponse({'notifications': data})

@login_required
def mark_notification_as_read(request, notification_id):
    """Mark a specific notification as read."""
    notification = get_object_or_404(UserNotification, id=notification_id, user=request.user)
    notification.mark_as_read()
    return JsonResponse({'status': 'success'})

@login_required
def notification_history(request):
    """Display all notifications for the user."""
    notifications_list = UserNotification.objects.filter(
        user=request.user,
        notification__is_active=True
    ).order_by('-notification__created_at')
    
    paginator = Paginator(notifications_list, 10) # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Notification/notifications_list.html', {'page_obj': page_obj})

# ─── Admin Management Views ──────────────────────────────────────────────────

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def admin_manage_notifications(request):
    """List all notifications for admin management."""
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'Notification/admin_manage_notifications.html', {'notifications': notifications})

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def admin_send_notification(request):
    """Create and broadcast a new notification."""
    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            messages.success(request, f"Notification '{notification.title}' has been sent to all users.")
            return redirect('admin_manage_notifications')
    else:
        form = NotificationForm()
    
    return render(request, 'Notification/admin_send_notification.html', {'form': form})

@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
def admin_delete_notification(request, notification_id):
    """Delete a notification."""
    if request.method == "POST":
        notification = get_object_or_404(Notification, notification_id=notification_id)
        title = notification.title
        notification.delete()
        messages.success(request, f"Notification '{title}' has been deleted.")
    return redirect('admin_manage_notifications')

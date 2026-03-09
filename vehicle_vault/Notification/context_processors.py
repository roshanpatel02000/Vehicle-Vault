from .models import UserNotification

def notification_count(request):
    if request.user.is_authenticated:
        count = UserNotification.objects.filter(user=request.user, is_read=False, notification__is_active=True).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}

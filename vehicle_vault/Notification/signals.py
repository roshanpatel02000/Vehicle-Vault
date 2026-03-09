from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, UserNotification
from core.models import User

@receiver(post_save, sender=Notification)
def create_user_notifications(sender, instance, created, **kwargs):
    if created and instance.is_active:
        users = User.objects.filter(is_active=True)
        user_notifications = [
            UserNotification(user=user, notification=instance)
            for user in users
        ]
        UserNotification.objects.bulk_create(user_notifications)

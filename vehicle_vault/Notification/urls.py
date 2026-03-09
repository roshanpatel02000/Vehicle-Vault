from django.urls import path
from . import views

urlpatterns = [
    path('fetch/', views.fetch_notifications, name='fetch_notifications'),
    path('mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('history/', views.notification_history, name='notification_history'),
    
    # Admin Views
    path('manage/', views.admin_manage_notifications, name='admin_manage_notifications'),
    path('send/', views.admin_send_notification, name='admin_send_notification'),
    path('delete/<uuid:notification_id>/', views.admin_delete_notification, name='admin_delete_notification'),
]

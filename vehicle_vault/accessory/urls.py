from django.urls import path
from . import views

urlpatterns = [
    path('', views.accessoryListView, name='accessories'),
    path("api/favourite/<int:accessory_id>/", views.toggle_favourite_accessory, name="toggle_favourite_accessory"),
    path("favourite-accessories/", views.favouriteAccessoriesView, name="favourite_accessories"),
    
    # Admin Management
    path('manage/', views.admin_manage_accessories, name='admin_manage_accessories'),
    path('add/', views.admin_add_accessory, name='admin_add_accessory'),
    path('edit/<int:accessory_id>/', views.admin_edit_accessory, name='admin_edit_accessory'),
    path('delete/<int:accessory_id>/', views.admin_delete_accessory, name='admin_delete_accessory'),
]

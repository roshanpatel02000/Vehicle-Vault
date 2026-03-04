from django.urls import path
from . import views

urlpatterns = [
    path("", views.homeView, name="home"),
    path("admin-dashboard/", views.AdminDashboardView, name="admin_dashboard"),
    path("admin-dashboard/users/", views.ManageUsersView, name="manage_users"),
    path("admin-dashboard/users/delete/<int:user_id>/", views.DeleteUserView, name="delete_user"),
    path("admin-dashboard/vehicles/", views.ManageVehiclesView, name="manage_vehicles"),
    path("admin-dashboard/vehicles/add/", views.AddVehicleView, name="add_vehicle"),
    path("admin-dashboard/vehicles/delete/<int:vehicle_id>/", views.DeleteVehicleView, name="delete_vehicle"),
    path("admin-dashboard/pending-admins/", views.PendingAdminsView, name="pending_admins"),
    path("admin-dashboard/approve-admin/<int:user_id>/", views.ApproveAdminView, name="approve_admin"),
    path("admin-dashboard/reject-admin/<int:user_id>/", views.RejectAdminView, name="reject_admin"),
    path("user-dashboard/", views.UserDashboardView, name="user_dashboard"),
    path("compare/", views.comparisonPageView, name="compare_vehicles"),
    path("compare/api/", views.compareVehiclesView, name="compare_vehicles_api"),
]
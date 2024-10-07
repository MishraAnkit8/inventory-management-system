from django.urls import path
from .views import   register_page, user_registration, login_page_view, login_view, render_dashbord_page, render_inventory_store, insert_inventory_details, inventory_details_update, deactivate_inventory

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # JWT Authentication URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('inventory/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('register/', register_page, name='register'),
    path('register/user-registration-data', user_registration, name='user_registration'),
    path('login/', login_page_view, name='login'),
    path('login/login-details', login_view, name='login-details'),
    path('dashboard/', render_dashbord_page, name='dashboard'),
    path('inventery/', render_inventory_store, name='inventory'),
    path('inventory/inventry-details', insert_inventory_details, name='inventory_details'),
    path('inventory/inventry-details-update', inventory_details_update , name='update_inventory_details'),
    path('inventory/delete', deactivate_inventory, name='deactivate-inventory')
]
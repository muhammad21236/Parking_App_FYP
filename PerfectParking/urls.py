"""PerfectParking URL Configuration"""
from django.urls import path
from . import views, WebPaths
from PerfectParking.views import custom_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('map/', views.map_view, name='map'),
    path(WebPaths.ROOT, views.index, name='home'),
    path('logout-user/', views.logout_user, name='logout-user'),

    path(WebPaths.PARKING_LOTS, views.parking_lots, name='parking-lots'),
    path(f'{WebPaths.PARKING_LOTS}/<int:parking_lot_id>/', views.parking_lot, name='parking-lot'),

    path(WebPaths.REGISTER_USER, views.register_user, name='register-user'),

    path(WebPaths.PARKING_LOT_MONITORS, views.parking_lot_monitors, name='parking-lot-monitors'),
    path(f'{WebPaths.PARKING_LOT_MONITOR}/<int:parking_lot_monitor_id>/', views.parking_lot_monitor, name='parking-lot-monitor'),

    path(WebPaths.PRIVACY_POLICY, views.privacy_policy, name='privacy-policy'),

    path("accounts/logout/", custom_logout, name="logout"),
    
        path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]

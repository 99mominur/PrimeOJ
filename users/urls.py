# from django.urls import path
# from .views import register, login_view, logout_view

# urlpatterns = [
#     path('register/', register, name='register'),
#     path('login/', login_view, name='login'),
#     path('logout/', logout_view, name='logout'),
# ]

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views  # Your custom views (for registration)

urlpatterns = [
    # Login view
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # Logout view
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    
    # Registration (custom view)
    path('register/', views.register, name='register'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('profile/', views.profile, name='profile'),

]
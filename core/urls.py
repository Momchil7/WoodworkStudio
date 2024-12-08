from django.urls import path

from content.views import user_favorites, view_user_favorites
from .views import UserRegistrationView, UserProfileUpdateView, index, DashboardView, \
    user_logout, user_login, UserProfileView, DirectPasswordResetView

app_name = 'core'

urlpatterns = [
    # Public Views
    path('', index, name='index'),  # Public landing page
    path('register/', UserRegistrationView.as_view(), name='register'),  # User registration
    path('login/', user_login, name='login'),  # User login
    path('logout/', user_logout, name='logout'),  # User logout

    # Private Views
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # User dashboard
    path('profile/', UserProfileView.as_view(), name='view_profile'),  # Current user
    path('profile/<str:username>/', UserProfileView.as_view(), name='view_profile_by_username'),  # Specific user
    path('profile/update', UserProfileUpdateView.as_view(), name='profile'),
    path('profile/<str:username>/favorites/', view_user_favorites, name='view_user_favorites'),

    path('password-reset/', DirectPasswordResetView.as_view(), name='password_reset'),
]
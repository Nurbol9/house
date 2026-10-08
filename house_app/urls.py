from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LoginView,
    LogoutView,
    UserProfileView,
    PropertyDetailView,
    PropertyListView,
    RegisterView,
    ReviewDetailView,
    ReviewListView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserProfileView.as_view(), name='profile'),
    path('property/', PropertyListView.as_view(), name='property-list'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('review/', ReviewListView.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
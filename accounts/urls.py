from django.urls import path
from . import views
from .views import list_users, promote_user, download_users, about, contact

urlpatterns = [
    path('', views.default_page, name='default'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', list_users, name='list_users'),
    path('promote_user/<int:user_id>/', promote_user, name='promote_user'),
    path('download_users/', download_users, name='download_users'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]

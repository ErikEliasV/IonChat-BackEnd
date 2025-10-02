from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('ping/', views.ping_user, name='ping'),
    path('me/', views.get_current_user, name='current_user'),
    path('', views.get_all_users, name='all_users'),
    path('<uuid:user_id>/', views.get_user_by_id, name='get_user'),
]

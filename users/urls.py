from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('<uuid:user_id>/', views.get_user_by_id, name='get_user'),
]

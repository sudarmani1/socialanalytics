from . import views
from django.urls import path, include

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login-view'),
    path('register/', views.RegisterView.as_view(), name='register-view'),
    path('logout/', views.LogoutView.as_view(), name='logout-view'),
]

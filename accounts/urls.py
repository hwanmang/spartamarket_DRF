from django.urls import path
from . import views

urlpatterns = [
    path('', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile_update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('delete/', views.DeleteAccountView.as_view(), name='delete_account'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('<str:username>/', views.Profile.as_view(), name='profile'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('update/', views.Update.as_view(), name='update'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('delete/', views.Delete.as_view(), name='delete'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='products'),
    path('<int:pk>/', views.UpdateProductView.as_view(), name='update_product'),
    path('<int:pk>/delete/', views.DeleteProductView.as_view(),
         name='delete_product'),
]

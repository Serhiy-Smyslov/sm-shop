from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:ct_model>/<str:slug>', views.ProductDetailView.as_view(), name='product_details'),
]

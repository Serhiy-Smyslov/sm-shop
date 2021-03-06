from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.BaseView.as_view(), name='home'),
    path('products/<str:slug>/', views.ProductDetailView.as_view(), name='product_details'),
    path('category/<str:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('make-order/', views.MakeOrderView.as_view(), name='make_order'),
    path('add-to-cart/<str:slug>/', views.AddView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:slug>/', views.DeleteView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', views.ChangeQTYView.as_view(), name='change_qty'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile')
]

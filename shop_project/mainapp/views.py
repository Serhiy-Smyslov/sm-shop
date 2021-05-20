from django.shortcuts import render
from django.views.generic import DetailView, ListView, View

from .models import Smartphone, Laptop, Category, LatestProducts, Customer, Cart
from .mixins import CategoryDetailMixin


# Create your views here.
class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('laptop', 'smartphone')
        context = {
            'categories': categories,
            'products': products,
        }
        return render(request, 'base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'laptop': Laptop,
        'smartphone': Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'category_detail.html'
    content_object_name = 'category'
    slug_url_kwarg = 'slug'


class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': cart,
            'categories': categories,
        }
        return render(request, 'cart.html', context)

from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Smartphone, Laptop


# Create your views here.
def home(request):
    return render(request, 'base.html')


class ProductDetailView(DetailView):

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

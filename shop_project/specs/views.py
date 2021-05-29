from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View


# Create your views here.
from specs.forms import NewCategoryForm, NewCategoryFeatureForm


class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'product_features.html', {})


class NewCategoryView(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/product-features/')
        return render(request, 'new_category.html', context)


class CreateNewFeature(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryFeatureForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_feature.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryFeatureForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            new_category_feature = form.save(commit=False)
            new_category_feature.category = form.cleaned_data['category']
            new_category_feature.feature_name = form.cleaned_data['feature_name']
            new_category_feature.save()
            return HttpResponseRedirect('/product-features/')
        return render(request, 'new_feature.html', context)
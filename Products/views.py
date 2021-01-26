from django.shortcuts import render
from .models import Products, Category
from django.http import HttpResponse
from django.views import generic


# Create your views here.


class ProductsView(generic.ListView):
    template_name = 'Products/Products.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Products.objects.all()


class ProductView(generic.DetailView):
    model = Products
    template_name = 'Products/Product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class MainView(generic.ListView):
    model = Category
    template_name = 'Products/Main.html'
    context_object_name = 'category_list'


class CategoriesView(generic.ListView):
    template_name = 'Products/Categories.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        return Category.objects.all()


class CategoryView(generic.DetailView):
    model = Category
    template_name = 'Products/Category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['product_in_cat'] = Products.objects.filter(category_id=self.object.id)
        return context



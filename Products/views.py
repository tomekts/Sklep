from django.shortcuts import render, redirect
from .models import Products, Category, Cart, CartProducts
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm


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


# class LoginView(generic.ListView):
#     model = User
#     context_object_name = 'user'
#     template_name = 'Products/Login.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = UserCreationForm
#         return context
def Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Products:Main')
        else:
            messages.info(request,'błedne hasło lub login')

    context={}
    return render(request, 'Products/Login.html', context)


def Logout(request):
    ss = request.META.get('PATH_INFO', None)
    print(request.session)
    logout(request)
    print(ss)
    return redirect('Products:Main')

def Register(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Products:Login')

    context = {'form': form}
    return render(request, 'Products/Register.html', context)


class CartView(generic.ListView):
    template_name = 'Products/Cart.html'
    context_object_name = 'category_list'

    def get_queryset(self):

        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.id)
        cart_id,bool = Cart.objects.filter(UserId=self.request.user.id).get_or_create(defaults={'UserId': self.request.user})
        context['products_in_cart'] = CartProducts.objects.filter(CartId=cart_id)
        context['products'] = Products.objects.all()
        return context

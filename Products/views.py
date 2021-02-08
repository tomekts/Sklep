from django.shortcuts import render, redirect
from .models import Products, Category, Cart, CartProducts
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import CreateUserForm, CartProductForm,  CartProductChangeCountForm




# Create your views here.


class ProductsView(generic.ListView):
    template_name = 'Products/Products.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Products.objects.all()


class ProductView(generic.DetailView):
    model = Products
    template_name = 'Products/Product.html'

    def post(self, request, pk):

        checkProductInCart= CartProducts.objects.filter(CartId=Cart.objects.get(UserId=self.request.user.id), ProductsId=pk )
        form = CartProductForm(request.POST)

        if not checkProductInCart:
            if form.is_valid():
                print('trs')
                form.save()
                messages.info(request, 'dodano produkt do koszyka')
        else:
            messages.info(request, 'produkt juz jest w koszyku')
        return redirect('Products:Product',pk)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        if self.request.user.is_authenticated:
            cartId,bool = Cart.objects.filter(UserId=self.request.user.id).get_or_create(defaults={'UserId': self.request.user})
            context['product_in_cat'] = CartProducts.objects.filter(CartId=cartId)
            context['cartid'] = cartId
            context['form'] = CartProductForm()
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

    def post(self, request, pk):
        form = CartProductForm(request.POST)
        idp = request.POST.get('product')
        checkProductInCart = CartProducts.objects.filter(CartId=Cart.objects.get(UserId=self.request.user.id), ProductsId=idp)
        if not checkProductInCart:
            if form.is_valid():
                form.save()
                messages.info(request, 'dodano produkt')
        else:
            messages.info(request, 'produkt juz w koszyku')
        return redirect('Products:Category',pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cartId,bool = Cart.objects.filter(UserId=self.request.user.id).get_or_create(defaults={'UserId': self.request.user})
            context['form'] = CartProductForm(initial={'CartId': cartId, 'ProductsId': self.object.id})
            context['cart'] = cartId

        context['category_list'] = Category.objects.all()
        context['product_in_cat'] = Products.objects.filter(category_id=self.object.id)

        return context


class Login(generic.TemplateView):
    template_name = 'Products/Login.html'

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Products:Main')
        else:
            return render(request, 'Products/Login.html',
                          messages.info(request,'błedne hasło lub login'))

    def get_queryset(self):
        return Category.objects.all()


class LogoutView(generic.TemplateView):
    template_name = 'Products/Main.html'

    def get(self,request):
        logout(request)
        return redirect('Products:Main')



class RegisterView (generic.TemplateView):
    template_name = 'Products/Register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateUserForm
        return context

    def post(self,request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Products:Login')
        context = {'form': form}
        return render(request, 'Products/Register.html', context)


class CartView(generic.ListView):
    template_name = 'Products/Cart.html'
    context_object_name = 'category_list'

    def post(self, request):
        if 'delete' in request.POST:
            cartid = request.POST.get('delete')
            item = CartProducts.objects.get(id=cartid)
            item.delete()
        if 'countChange' in request.POST:
            item = CartProducts.objects.get(id=request.POST.get('product'))
            form = CartProductChangeCountForm(request.POST or None, instance=item)
            if form.is_valid():
                form.save()
        return redirect('Products:Cart')

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id,bool = Cart.objects.filter(UserId=self.request.user.id)\
            .get_or_create(defaults={'UserId': self.request.user})
        context['products_in_cart'] = CartProducts.objects.filter(CartId=cart_id)
        context['formChange'] = CartProductChangeCountForm
        context['cart'] = Cart
        return context


class UserChangPasswordView(generic.TemplateView):
    template_name = 'Products/User-password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['form'] = PasswordChangeForm(self.request.user)
        return context

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'hasło zostało zmienione')
        else:
             messages.info(request, 'hasło nie zostało zmienione')


        return redirect('Products:User')


class UserView(generic.TemplateView):
    template_name = 'Products/User.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['form'] = PasswordChangeForm(self.request.user)
        return context












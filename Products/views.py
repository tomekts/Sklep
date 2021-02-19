from django.shortcuts import render, redirect
from .models import Products, Category, Cart, CartProducts, Producer
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import CreateUserForm, CartProductForm, CartProductChangeCountForm, EditProfilForm
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, ProductsSerializer, CategorySerializer, CartSerializer, CartProductsSerializer, ProducerSerializer
from django.core.paginator import Paginator
from .filters import ProductFilter
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin



def send_email(subject, adress, massage, request):
    if adress:
        msg = EmailMultiAlternatives(
            # sumbejct
            subject,
            # content
            # to
            to=[adress],
            # from
            from_email='',
        )
        msg.attach_alternative(massage, "text/html")
        msg.send()
        messages.info(request, 'Email został wysłany')
    else:
        messages.info(request, 'wpisz adres')

class ProducerView(generic.DetailView):
    template_name = 'Products/Producer.html'
    context_object_name = 'producer_list'
    model = Producer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class ProductView(generic.DetailView):
    model = Products
    template_name = 'Products/Product.html'


    def post(self, request, pk):
        cart_id_user = Cart.objects.get(UserId=self.request.user.id)
        check_product_in_cart= CartProducts.objects.filter(CartId=cart_id_user, ProductsId=pk)
        form = CartProductForm(request.POST)

        if not check_product_in_cart:
            if form.is_valid():
                form.save()
                messages.info(request, 'dodano produkt do koszyka')
        else:
            messages.info(request, 'produkt juz jest w koszyku')
        return redirect('Products:Product', pk)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        if self.request.user.is_authenticated:
            cart_id, bool = Cart.objects.filter(UserId=self.request.user.id).get_or_create(defaults={'UserId': self.request.user})
            context['product_in_cat'] = CartProducts.objects.filter(CartId=cart_id)
            context['cartid'] = cart_id
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
        id_product = request.POST.get('product')
        cart_id_user = Cart.objects.get(UserId=self.request.user.id)
        check_product_in_cart = CartProducts.objects.filter(CartId=cart_id_user, ProductsId=id_product)
        paginate_by = 2
        if not check_product_in_cart:
            if form.is_valid():
                form.save()
                messages.info(request, 'dodano produkt')
        else:
            messages.info(request, 'produkt juz w koszyku')
        return redirect('Products:Category', pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id, bool = Cart.objects.filter(UserId=self.request.user.id).get_or_create(defaults={'UserId': self.request.user})
            context['form'] = CartProductForm(initial={'CartId': cart_id, 'ProductsId': self.kwargs.get('pk')})
            context['cart'] = cart_id

        context['category_list'] = Category.objects.all()
        # context['product_in_cat'] = Products.objects.filter(category_id=self.kwargs.get('pk'))
        product = Products.objects.filter(category_id=self.kwargs.get('pk'))
        product_filter = ProductFilter(self.request.GET, queryset=product)

        pag = Paginator(product_filter.qs, 4)
        page_num = self.request.GET.get('page', 1)
        try:
            page = pag.page(page_num)
        except:
            page=pag.page(1)
        context['name'] = 'test'
        context['product_filter'] = product_filter
        context['product_pagination'] = page
        return context


class SearchView(generic.ListView):
    model = Category
    template_name = 'Products/Search.html'
    context_object_name = 'category'

    def post(self, request):
        form = CartProductForm(request.POST)
        id_product = request.POST.get('product')
        cart_id_user = Cart.objects.get(UserId=self.request.user.id)
        check_product_in_cart = CartProducts.objects.filter(CartId=cart_id_user, ProductsId=id_product)
        paginate_by = 2
        if not check_product_in_cart:
            if form.is_valid():
                form.save()
                messages.info(request, 'dodano produkt')
        else:
            messages.info(request, 'produkt juz w koszyku')

        return redirect('Products:Search')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_id, bool = Cart.objects.filter(UserId=self.request.user.id).get_or_create(
                defaults={'UserId': self.request.user})
            context['form'] = CartProductForm(initial={'CartId': cart_id, 'ProductsId': self.kwargs.get('pk')})
            context['cart'] = cart_id

        context['category_list'] = Category.objects.all()
        # context['product_in_cat'] = Products.objects.filter(category_id=self.kwargs.get('pk'))
        product = Products.objects.all()
        product_filter = ProductFilter(self.request.GET, queryset=product)

        pag = Paginator(product_filter.qs, 4)
        page_num = self.request.GET.get('page', 1)
        try:
            page = pag.page(page_num)
        except:
            page = pag.page(1)
        context['name'] = 'test'
        context['product_filter'] = product_filter
        context['product_pagination'] = page
        return context

class Login(generic.TemplateView):
    template_name = 'Products/Login.html'

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(request)
        if user is not None:
            login(request, user)
            return redirect('Products:Main')
        else:
            return render(request, 'Products/Login.html',
                          messages.info(request, 'błedne hasło lub login'))

    def get_queryset(self):
        return Category.objects.all()


class LogoutView(generic.TemplateView):
    template_name = 'Products/Main.html'

    def get(self, request):
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
            cart_id = request.POST.get('delete')
            item = CartProducts.objects.get(id=cart_id)
            item.delete()
        if 'countChange' in request.POST:
            item = CartProducts.objects.get(id=request.POST.get('product'))
            form = CartProductChangeCountForm(request.POST or None, instance=item)
            if form.is_valid():
                form.save()
        if 'send' in request.POST:
            adress = request.POST.get('mail')
            # item = CartProducts.objects.filter(CartId=3)
            cart_id = Cart.objects.get(UserId = request.user.id)
            context = {'product': Products.objects.all()}
            context['cart'] = CartProducts.objects.filter(CartId=cart_id)
            file = render_to_string('test.html', context, request)
            send_email("Twój koszyk", adress,file, request)
        return redirect('Products:Cart')

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id, bool = Cart.objects.filter(UserId=self.request.user.id)\
            .get_or_create(defaults={'UserId': self.request.user})
        context['products_in_cart'] = CartProducts.objects.filter(CartId=cart_id)
        context['formChange'] = CartProductChangeCountForm
        context['cart'] = Cart
        return context

class UserChangPasswordView(PasswordChangeView, SuccessMessageMixin):
    from_class = PasswordChangeForm
    template_name = 'Products/User-password.html'
    success_url = '/user/'

    def form_valid(self, form):
        messages.info(self.request, 'Hasło zostało zmienione')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class UserView(generic.UpdateView, SuccessMessageMixin):
    form_class = EditProfilForm
    success_url = '/user/'
    template_name = 'Products/User.html'

    def form_valid(self, form):
        messages.info(self.request, 'dane zostały zapiasne')
        form.save()
        return redirect('Products:User')


    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    #permission_classes = [permissions.IsAdminUser]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [permissions.IsAdminUser]


class ProducerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    #permission_classes = [permissions.IsAdminUser]


class CartProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CartProducts.objects.all()
    serializer_class = CartProductsSerializer
    #permission_classes = [permissions.IsAdminUser]

class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    #permission_classes = [permissions.IsAdminUser]












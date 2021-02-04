
from django.contrib.auth.forms import UserCreationForm
from .models import CartProducts, Products,Cart
from django.contrib.auth.models import User
from django import forms





class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CartProductForm(forms.ModelForm):
    product = forms.IntegerField()
    cart = forms.IntegerField()

    class Meta:
        model = CartProducts
        fields = ['Count']


    def save(self, commit=True ):
        instance = super(CartProductForm, self).save(commit=False)
        instance.ProductsId = Products.objects.get(pk=self.data['product'])
        instance.CartId = Cart.objects.get(pk=self.data['cart'])
        instance.save()


class CartProductDeleteForm(forms.ModelForm):
    class Meta:
        model = CartProducts
        fields = ['CartId']







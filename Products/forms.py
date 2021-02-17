
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CartProducts, Products,Cart
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditProfilForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']



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


class CartProductChangeCountForm(forms.ModelForm):
    product = forms.IntegerField()

    class Meta:
        model = CartProducts
        fields = ['Count']

    def save(self, commit=True ):
        instance = super(CartProductChangeCountForm, self).save(commit=False)
        if int(self.data['Count']) <=0:
            print('ponizej zera')
            instance.Count =1
        else:
            instance.Count = self.data['Count']
        instance.CartId = CartProducts.objects.get(pk=self.data['product']).CartId

        instance.save()







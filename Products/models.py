from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email addres'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Producer(models.Model):
    def urla(self, filename):
        return os.path.join('images/logo/', filename)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=urla, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Producent'
        verbose_name_plural = 'Producenci'




class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'


class Products(models.Model):

    def urla(self, filename):
        return os.path.join('images/product', filename)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to=urla,null=True)

    def __str__(self):
        if len(self.title)>50:
            return self.title[:50]+'...'
        return self.title

    class Meta:
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkty'


class CartProducts(models.Model):
    CartId = models.ForeignKey('cart', on_delete=models.CASCADE, null=True)
    ProductsId = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    Count = models.IntegerField()

    def SumPrice(self):
        return self.ProductsId.price * self.Count

    def SumPriceAll(self):
        sum=0
        Listprod=CartProducts.objects.filter(CartId= self.CartId)
        for i in Listprod:
            sum += i.Count * i.ProductsId.price
        return sum


class Cart(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk)








from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.


class Producer(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

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

        return os.path.join('images/', filename)

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

    def up(self):
        return 'www'


class Cart(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk)








from django.contrib import admin
from .models import Products, Producer, Category, CartProducts, Cart
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'UserId')

class CartProductsAdmin(admin.ModelAdmin):
    list_display = ('CartId', 'ProductsId', 'Count')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'producer', 'price')
    list_filter = ('producer', 'category')


admin.site.register(Category)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProducts, CartProductsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Producer)





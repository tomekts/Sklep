from django.contrib import admin
from .models import Products, Producer, Category, CartProducts, Cart
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'UserId')

class CartProductsAdmin(admin.ModelAdmin):
        list_display = ('CartId', 'ProductsId', 'Count')


admin.site.register(Category)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProducts, CartProductsAdmin)
admin.site.register(Products)
admin.site.register(Producer)





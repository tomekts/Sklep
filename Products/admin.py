from django.contrib import admin
from .models import Products, Producer, Category, CartProducts, Cart
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'UserId')


class CartProductsAdmin(admin.ModelAdmin):
    list_display = ('CartId', 'ProductsId', 'Count')


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'producer', 'price')
    list_filter = ('producer', 'category')


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Category)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProducts, CartProductsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Producer)
admin.site.register(get_user_model(), CustomUserAdmin)





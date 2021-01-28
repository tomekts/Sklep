from django.urls import path
from Products.views import *
from . import views

app_name = 'Products'
urlpatterns = [
    path('', views.MainView.as_view(), name='Main'),
    path('products/', views.ProductsView.as_view(), name='Products'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='Product'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='Category'),
    path('category/', views.CategoriesView.as_view(), name='Categories'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('register/', views.Register, name='Register'),


]
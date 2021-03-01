from django.urls import path, include

from . import views


from rest_framework import routers

app_name = 'Products'
urlpatterns = [
    path('', views.MainView.as_view(), name='Main'),
    # path('products/', views.ProductsView.as_view(), name='Products'),
    path('products/<int:pk>/', views.ProductView.as_view(), name='Product'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='Category'),
    # path('category/', views.CategoriesView.as_view(), name='Categories'),
    path('login/', views.Login.as_view(), name='Login'),
    path('logout/', views.LogoutView.as_view(), name='Logout'),
    path('register/', views.RegisterView.as_view(), name='Register'),
    path('cart/', views.CartView.as_view(), name='Cart'),
    path('password/', views.UserChangPasswordView.as_view(), name='User-password'),
    path('user/', views.UserView.as_view(), name='User'),
    path('producer/<int:pk>/', views.ProducerView.as_view(), name='Producer'),
    path('search/', views.SearchView.as_view(), name='Search'),
    path('register_done/', views.RegisterDone.as_view(), name='register_done'),
    path('reset_password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_sent/', views.ResetPasswordDoneForm.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete', views.ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>',views.VerificationView.as_view(), name='activate'),
]

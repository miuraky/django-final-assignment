from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'final'
urlpatterns = [
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='final:login'), name='logout'),

    path('', views.DashboardView.as_view(), name='index'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/filter/', views.filtered_products,name='filtered_products'),

    path('stock/<int:pk>/change/', views.StockChangeView.as_view(), name='stock_change'),
    path('history/', views.StockHistoryView.as_view(), name='stock_history'),
]
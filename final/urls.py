# from django.urls import path, include
# from . import views

# app_name = 'final'

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),  #一覧ページのビュー
#     path('products/filtered/', views.products, name='filtered_products'),

# ]


# final/urls.py
from django.urls import path
from . import views

app_name = 'final'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/filtered/', views.filtered_products, name='filtered_products'),
]
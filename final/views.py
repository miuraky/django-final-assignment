from django.shortcuts import render, redirect
from django.views import generic
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy

class IndexView(generic.ListView):
    model = Product
    template_name = 'final/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = Product.objects.count()
        context['out_of_stock_count'] = Product.objects.filter(stock=0).count()
        context['low_stock_count'] = Product.objects.filter(stock__lt=10).exclude(stock=0).count()
        return context

class ProductListView(generic.ListView):
    model = Product
    template_name = 'final/product_list.html'
    context_object_name = 'products'

class ProductCreateView(generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'final/product_form.html'
    success_url = reverse_lazy('final:product_list')

def filtered_products(request):
    filter_type = request.GET.get('filter')
    if filter_type == 'out_of_stock':
        products = Product.objects.filter(stock=0)
        title = "在庫切れ商品"
    elif filter_type == 'low_stock':
        products = Product.objects.filter(stock__lt=10).exclude(stock=0)
        title = "在庫少ない商品（10個未満）"
    else:
        products = Product.objects.all()
        title = "すべての商品"
    
    return render(request, 'final/product_list.html', {
        'products': products,
        'title': title,
    })

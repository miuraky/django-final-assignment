from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Product, StockHistory
from .forms import ProductForm, StockHistoryForm
import django.db.models as models

# ダッシュボード
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'final/index.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_qs = Product.objects.all()
        ctx['total_products']    = all_qs.count()
        ctx['out_of_stock_count'] = all_qs.filter(stock=0).count()
        ctx['low_stock_count']   = all_qs.filter(stock__lt=10).exclude(stock=0).count()
        return ctx

# 商品一覧・検索
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'final/product_list.html'
    context_object_name = 'products'
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        return qs.filter(models.Q(code__icontains=q) | models.Q(name__icontains=q))
    
    

# 商品作成・更新
class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'final/product_form.html'
    success_url = reverse_lazy('final:product_list')
    permission_required = 'final.add_product'

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'final/product_form.html'
    success_url = reverse_lazy('final:product_list')
    permission_required = 'final.change_product'

# 在庫移動フォーム
class StockChangeView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'final/stock_change.html'
    form_class = StockHistoryForm
    permission_required = 'final.add_stockhistory'

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        hist = form.save(commit=False)
        hist.product = product
        hist.operated_by = self.request.user

        # ✅ 在庫チェック（履歴保存より前に）
        if hist.movement_type == 'out' and hist.quantity > product.stock:
            form.add_error('quantity', f'在庫が不足しています（現在の在庫: {product.stock}）')
            return self.form_invalid(form)

        # ✅ 在庫更新
        if hist.movement_type == 'in':
            product.stock += hist.quantity
        else:
            product.stock -= hist.quantity

        product.save()
        hist.save()  # ← 在庫に問題がないことを確認してから保存
        return redirect('final:product_list')


# 履歴一覧
class StockHistoryView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = StockHistory
    template_name = 'final/stock_history.html'
    paginate_by = 20
    permission_required = 'final.view_stockhistory'

    
def filtered_products(request):
    filter_type = request.GET.get('filter')

    if filter_type == 'out_of_stock':
        products = Product.objects.filter(stock=0)
        title = "在庫切れの商品一覧"
    elif filter_type == 'low_stock':
        products = Product.objects.filter(stock__lt=10)
        title = "低在庫の商品一覧"
    else:
        products = Product.objects.all()
        title = "全商品一覧"

    context = {
        'products': products,
        'title': title,
    }

    return render(request, 'final/filtered_products.html', context)


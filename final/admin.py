from django.contrib import admin

# Register your models here.
from .models import Product # models.pyからProductクラスをインポート
from .models import StockHistory # models.pyからStockHistoryクラスをインポート

admin.site.register(Product)    # DjangoAdminにProductクラスを登録
admin.site.register(StockHistory)   # DjangoAdminにStockHistoryクラスを登録
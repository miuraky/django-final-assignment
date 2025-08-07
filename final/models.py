# from django.db import models
# import uuid

# # Create your models here.

# class Product(models.Model):
#     code = models.CharField(max_length=30, unique=True)  # 品番（SKU）
#     name = models.CharField(max_length=100)
#     category = models.CharField(max_length=50, blank=True)
#     unit = models.CharField(max_length=10, default='個')  # kg, 箱, 個など
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # ←追加！
#     stock = models.IntegerField(default=0)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.code} - {self.name}"
    
#     def save(self, *args, **kwargs):
#         if not self.code:
#             self.code = str(uuid.uuid4())[:8]  # 例：8桁のユニークなコード
#         super().save(*args, **kwargs)


# class StockHistory(models.Model):
#     IN_OUT_CHOICES = (
#         ('in', '入庫'),
#         ('out', '出庫'),
#     )

#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     movement_type = models.CharField(max_length=3, choices=IN_OUT_CHOICES)
#     quantity = models.IntegerField()
#     operated_by = models.CharField(max_length=50)  # 操作した人の名前 or ID
#     remarks = models.TextField(blank=True)  # メモや理由
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.get_movement_type_display()} {self.quantity} → {self.product.name}"

from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    code = models.CharField('SKU', max_length=30, unique=True, blank=True)
    name = models.CharField('商品名', max_length=100)
    category = models.CharField('カテゴリー', max_length=50, blank=True)
    unit = models.CharField('単位', max_length=10, default='個')
    price = models.DecimalField('定価', max_digits=10, decimal_places=2)

    stock = models.IntegerField('在庫数', default=0)
    minimum_stock = models.IntegerField('最低在庫数', default=0)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

class StockHistory(models.Model):
    IN_OUT_CHOICES = (
        ('in', '入庫'),
        ('out', '出庫'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField('種別', max_length=3, choices=IN_OUT_CHOICES)
    quantity      = models.IntegerField('数量')
    operated_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='担当者')
    remarks       = models.TextField('備考', blank=True)
    timestamp     = models.DateTimeField('日時', auto_now_add=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity} → {self.product.name} @ {self.timestamp:%Y-%m-%d %H:%M}"
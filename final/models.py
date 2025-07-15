from django.db import models

# Create your models here.

class Product(models.Model):
    code = models.CharField(max_length=30, unique=True)  # 品番（SKU）
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True)
    unit = models.CharField(max_length=10, default='個')  # kg, 箱, 個など
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ←追加！
    stock = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class StockHistory(models.Model):
    IN_OUT_CHOICES = (
        ('in', '入庫'),
        ('out', '出庫'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=3, choices=IN_OUT_CHOICES)
    quantity = models.IntegerField()
    operated_by = models.CharField(max_length=50)  # 操作した人の名前 or ID
    remarks = models.TextField(blank=True)  # メモや理由
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity} → {self.product.name}"

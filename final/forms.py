# from django import forms
# from .models import Product

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'category', 'stock', 'price']

from django import forms
from .models import Product, StockHistory

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['code', 'name', 'category', 'unit', 'price', 'minimum_stock']
# from django import forms
# from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price']  # 必要に応じて
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：りんご'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例：果物'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '例：100'}),
        }


class StockHistoryForm(forms.ModelForm):
    class Meta:
        model = StockHistory
        fields = ['movement_type', 'quantity', 'remarks']
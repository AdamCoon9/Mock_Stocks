from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user.username} - {self.stock.name}'
    
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'current_price')
    ordering = ['name']
    search_fields = ('name', 'symbol')

class TradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'shares', 'price')
    ordering = ['user']
    list_filter = ('user', 'stock')

admin.site.register(Stock, StockAdmin)
admin.site.register(Trade, TradeAdmin)

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.IntegerField()
    average_purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

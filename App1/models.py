from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.FloatField()

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

class Holding(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    num_shares = models.IntegerField()

    average_purchase_price = models.FloatField()

class Transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    num_shares = models.IntegerField()

    transaction_price = models.FloatField()

    transaction_date = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000)  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

from django.contrib import admin
from .models import stock, Trade, Portfolio

admin.site.register(stock)
admin.site.register(Trade)
admin.site.register(Portfolio)

from django.contrib import admin
from django.urls import path
from . import views
from .views import reset_account, buy_stock_view, sell_stock_view, transaction_history_view, stocks_view, GetStockInfoView

urlpatterns = [
    path('create_profile/', views.register_and_create_profile, name='create_profile_view'),
    path('login/', views.login, name='login'),
    path('reset_account/', views.reset_account, name='reset_account'),
    path('buy_stock_view/', views.buy_stock_view, name='buy_stock_view'),
    path('sell_stock_view/', views.sell_stock_view, name='sell_stock_view'),
    path('transaction_history/', views.transaction_history_view, name='transaction_history'),
    path('stocks/', views.stocks_view, name='stocks'),
    path('get_stock_info/', GetStockInfoView.as_view(), name='get_stock_info'),
    
]


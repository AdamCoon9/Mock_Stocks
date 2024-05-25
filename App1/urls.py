
from django.urls import path
from . import views
from .views import reset_account
from .views import trading_screen_view
urlpatterns = [
    path('', views.home, name='home'),
    path('reset_account/', reset_account, name='reset_account'),
    path('trading_screen/', trading_screen_view, name='trading_screen'),

]

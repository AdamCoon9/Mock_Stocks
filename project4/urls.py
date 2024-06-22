"""
URL configuration for project4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Project4_App_level.Project4_App_level import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('Project4_App_level.Project4_App_level.urls')),
    path('register', views.register_and_create_profile, name='register'),
    path('login', views.login_request, name='login'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('stocks/', views.Stock, name='stocks'),
    path('buy_stock_view/', views.buy_stock_view, name='buy_stock_view'),
    path('sell_stock_view/', views.sell_stock_view, name='sell_stock_view'),
    path('profile/', views.profile, name='profile'),
]

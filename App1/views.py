from django.shortcuts import render, redirect
from django.db import models
from .forms import TradeForm
from django.http import JsonResponse
from .models import Portfolio
from django.contrib import messages
from .models import Transaction, UserProfile
from django.shortcuts import render
from .utils import get_stock_prices

def trading_screen_view(request):
    stock_prices = get_stock_prices()
    return render(request, 'trading_screen.html', {'stock_prices': stock_prices})

def trade_view(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data['stock']
            shares = form.cleaned_data['shares']
            action = form.cleaned_data['action']
            # Update the user's portfolio and balance
            # ...
            return redirect('portfolio')
    else:
        form = TradeForm()
    return render(request, 'trade.html', {'form': form})

def portfolio_view(request):
    # Fetch the user's holdings
    holdings = Portfolio.objects.filter(user=request.user)

    # Calculate the current value of each holding
    for holding in holdings:
        holding.current_value = holding.shares * holding.stock.current_price

    # Render the portfolio view
    return render(request, 'portfolio.html', {'holdings': holdings})

def transaction_history_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')
    return render(request, 'transaction_history.html', {'transactions': transactions})

def chart_data(request):
    data = Transaction.objects.filter(user=request.user).values('stock__symbol').annotate(total=models.Sum('num_shares'))
    chart_data = list(data)
    return JsonResponse(chart_data, safe=False)

import requests
def news_feed_view(request):

    response = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=0db4787f807647fd827bbd12f404442a')

    articles = response.json().get('articles', [])

    return render(request, 'news_feed.html', {'articles': articles})


def reset_account(request):
    # Check if the request is POST
    if request.method == 'POST':
        # Reset the user's balance
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.balance = 10000  # Set the balance back to the initial amount
        user_profile.save()

        # Delete all the user's transactions
        Transaction.objects.filter(user=request.user).delete()

        # Show a success message
        messages.success(request, 'Your account has been reset.')

        # Redirect to the portfolio page
        return redirect('portfolio')

    # If the request is not POST, you can redirect the user or show an error
    return redirect('home')

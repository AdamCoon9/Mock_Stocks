# Python standard library imports
from collections import defaultdict
from datetime import timedelta

# Third-party imports (Django)
from django.shortcuts import render, redirect
from django.db import models
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView 
from django.views import View
from django import forms
from django.template.loader import render_to_string
from django.template import engines
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Local application imports
from .forms import TradeForm, BuyStockForm, SellStockForm, UserRegisterForm, UserProfileForm
from .models import Portfolio, Stock, Transaction, UserProfile, UserStock
from Project4_App_level.Project4_App_level.models import Stock, UserProfile
from .models import UserProfile
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import yfinance as yf
from .utils import fetch_and_plot

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form, 'user_profile': user_profile})  # Pass 'user_profile' here


def update_portfolio(user):
    # Get all transactions for the user
    transactions = Transaction.objects.filter(user=user)

    # Iterate over all transactions
    for transaction in transactions:
        # Get or create the portfolio for the stock
        portfolio, created = Portfolio.objects.get_or_create(
            user=user, 
            stock=transaction.stock, 
            defaults={'shares': 0, 'average_purchase_price': transaction.transaction_price}
        )

        # If the portfolio was just created, set the shares and average_purchase_price
        if created:
            portfolio.shares = transaction.num_shares
            portfolio.average_purchase_price = transaction.transaction_price
        else:
            # If the portfolio already existed, update the shares and average_purchase_price
            total_shares = portfolio.shares + transaction.num_shares
            portfolio.average_purchase_price = ((portfolio.average_purchase_price * portfolio.shares) + (transaction.transaction_price * transaction.num_shares)) / total_shares
            portfolio.shares = total_shares

        # Save the updated portfolio
        portfolio.save()

class GetStockInfoView(View):
    def get(self, request, *args, **kwargs):
        stock_id = request.GET.get('stock_id')
        selected_stock = Stock.objects.get(id=stock_id)  # Assuming 'Stock' is your model name
        symbol = selected_stock.symbol  # Assuming 'symbol' is a field in your 'Stock' model

        if not symbol:
            return JsonResponse({'error': 'No symbol provided'}, status=400)

        data = yf.download(symbol, '2016-01-01', '2024-06-01')

        # Generate the plot
        plt.figure(figsize=(10,5))
        plt.plot(data['Close'])
        plt.title(f'{symbol} Close Price')

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = base64.b64encode(buf.read()).decode()

        # Include the image in your response data
        response_data = {
            'image': image,
        }

        user_has_stock = Portfolio.objects.filter(user=request.user, stock=selected_stock).exists()

        # Create the forms
        buy_form = BuyStockForm()
        sell_form = SellStockForm(user=request.user)  # Pass the user to the sell form

        # Render the forms to strings of HTML
        buy_form_html = render_to_string('buy_stock_form.html', {'buy_form': buy_form})
        sell_form_html = render_to_string('sell_stock_form.html', {'sell_form': sell_form})  # Render the sell form to HTML

        # Include the form HTML in your response data
        response_data.update({
            'price': str(selected_stock.current_price),
            'user_has_stock': user_has_stock,
            'buy_form_html': buy_form_html,
            'sell_form_html': sell_form_html,  
        })

        return JsonResponse(response_data)





class MyPasswordResetView(PasswordResetView):
                template_name = './password_reset_form.html'
def home(request):
    return render(request, './home.html')

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Invalid login credentials
            return render(request, './login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, './login.html')
    

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    balance = forms.DecimalField(max_digits=10, decimal_places=2, max_value=10000)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "balance",)



 # assuming you have a Profile model

def register_and_create_profile(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Check if the passwords match
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(request, './create_profile.html', {'form': form})

            # Save the user
            try:
                user = form.save()
            except Exception as e:
                messages.error(request, 'Error creating user: {}'.format(e))
                return render(request, './create_profile.html', {'form': form})

            # Create and save the profile
            profile = UserProfile(user=user)
            profile.save()

            messages.success(request, 'Your profile was successfully created.')
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = RegisterForm()

    return render(request, './create_profile.html', {'form': form})




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
    return render(request, './trade.html', {'form': form})

@login_required
def portfolio_view(request):
    if request.user.is_authenticated:
        # Fetch the user's UserProfile
        user_profile = UserProfile.objects.get(user=request.user)

        # Fetch the user's holdings
        holdings = UserStock.objects.filter(user=user_profile)

        # Calculate the current value of each holding
        for holding in holdings:
            holding.current_value = holding.quantity * holding.stock.current_price

        # Render the portfolio view
        return render(request, './portfolio.html', {'holdings': holdings})
    else:
        return redirect('login') 



def transaction_history_view(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user).order_by('transaction_date')

        # Calculate the daily value of the portfolio
        portfolio_value = defaultdict(float)
        for transaction in transactions:
            date = transaction.transaction_date.date()
            portfolio_value[date] += transaction.num_shares * transaction.transaction_price

        print(f'Portfolio value before filling missing dates: {portfolio_value}')  # Debugging line

        # Fill in the missing dates
        if portfolio_value:  # Check if portfolio_value is not empty
            min_date = min(portfolio_value.keys())
            max_date = max(portfolio_value.keys())
            date = min_date
            while date <= max_date:
                if date not in portfolio_value:
                    portfolio_value[date] = portfolio_value[date - timedelta(days=1)]
                date += timedelta(days=1)

        print(f'Portfolio value after filling missing dates: {portfolio_value}')  # Debugging line

        # Convert the dates to strings
        portfolio_value = sorted((date.strftime('%Y-%m-%d'), value) for date, value in portfolio_value.items())

        return render(request, './transaction_history.html', {
            'transactions': transactions,
            'portfolio_value': portfolio_value,
        })
    else:
        return redirect('login') 
def chart_data(request):
    data = Transaction.objects.filter(user=request.user).values('stock__symbol').annotate(total=models.Sum('num_shares'))
    chart_data = list(data)
    return JsonResponse(chart_data, safe=False)

import requests
def news_feed_view(request):

    response = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=0db4787f807647fd827bbd12f404442a')

    articles = response.json().get('articles', [])

    return render(request, './news_feed.html', {'articles': articles})


@login_required
def reset_account(request):
    print("Reset account view called")
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.balance = 10000  
        user_profile.save()

        # Reset the quantity of each UserStock for the user
        UserStock.objects.filter(user=user_profile).update(quantity=0)

        Transaction.objects.filter(user=request.user).delete()
        messages.success(request, 'Your account has been reset.')
        return redirect('portfolio')

    return redirect('profile')

def buy_stock_view(request):
    form = BuyStockForm(request.POST or None)  # Instantiate form here

    if request.method == 'POST':
        if form.is_valid():
            stock = form.cleaned_data['stock']
            quantity = form.cleaned_data['quantity']
            total_cost = stock.current_price * quantity

            # Check if the user has enough balance
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.balance >= total_cost:
                # Subtract the total cost from the user's balance
                user_profile.balance -= float(total_cost)
                user_profile.save()

                # Create a new transaction
                Transaction.objects.create(
                    user=request.user,
                    stock=stock,
                    num_shares=quantity,
                    transaction_price=stock.current_price,
                )

                # Update the user's UserStock
                user_stock, created = UserStock.objects.get_or_create(
                    user=user_profile, 
                    stock=stock, 
                    defaults={'quantity': 0}
                )
                if created:
                    user_stock.quantity = quantity
                else:
                    user_stock.quantity += quantity
                user_stock.save()

                # If the form is valid and the user has enough balance
                return JsonResponse({'result': 'success', 'buy_form_html': render_to_string('buy_stock_form.html', {'buy_form': form})})

            # If the form is valid but the user doesn't have enough balance
            return JsonResponse({'result': 'error', 'errors': form.errors, 'buy_form_html': render_to_string('buy_stock_form.html', {'buy_form': form})})

        # If the form is not valid
        return JsonResponse({'result': 'error', 'errors': form.errors, 'buy_form_html': render_to_string('buy_stock_form.html', {'buy_form': form})})

    # If the request method is not POST
    return JsonResponse({'buy_form_html': render_to_string('buy_stock_form.html', {'buy_form': form})})

def sell_stock_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':  # Check if the request is an AJAX request
        form = SellStockForm(request.POST, user=request.user)
        print(f'Received POST request: {request.POST}')
        if form.is_valid():
            print('Form is valid')
            stock = form.cleaned_data['stock']
            quantity = form.cleaned_data['quantity']




            # Fetch the user's UserProfile
            user_profile = UserProfile.objects.get(user=request.user)

            # Fetch the user's holdings
            holding = UserStock.objects.filter(user=user_profile, stock=stock)

            print("holding")
            print(holding)
            user_stock_quantity = 0
            for h in holding:
                user_stock_quantity += h.quantity

            # Check if the user owns enough of this stock to sell
            if user_stock_quantity >= quantity:
                  # Update the user's UserStock
                user_stock, created = UserStock.objects.get_or_create(
                    user=user_profile, 
                    stock=stock, 
                    defaults={'quantity': 0}
                )
                if created:
                    user_stock.quantity = (quantity * -1)
                else:
                    user_stock.quantity += (quantity * -1)
                user_stock.save()


                # Add the total cost to the user's balance
                total_cost = stock.current_price * quantity
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.balance += float(total_cost)
                user_profile.save()

                # Create a new transaction
                Transaction.objects.create(
                    user=request.user,
                    stock=stock,
                    num_shares=-quantity,
                    transaction_price=stock.current_price,
                )

                # Update the user's portfolio
                portfolio, created = Portfolio.objects.get_or_create(
                    user=request.user,
                    stock=stock,
                    defaults={'shares': 0, 'average_purchase_price': stock.current_price}
                )
                print(f'User shares before update: {portfolio.shares}')
                if created:
                    portfolio.shares = quantity
                    portfolio.average_purchase_price = stock.current_price
                else:
                    total_shares = portfolio.shares - quantity
                    portfolio.average_purchase_price = ((portfolio.average_purchase_price * portfolio.shares) - (stock.current_price * quantity)) / total_shares
                    portfolio.shares = total_shares
                print(f'User shares after update: {portfolio.shares}')
                portfolio.save()

                return JsonResponse({'result': 'success', 'sell_form_html': render_to_string('sell_stock_form.html', {'sell_form': form}, request=request)})
            else:
                form.add_error(None, 'You do not own enough of this stock to sell.')
                return JsonResponse({'result': 'error', 'errors': form.errors, 'sell_form_html': render_to_string('sell_stock_form.html', {'sell_form': form}, request=request)})
        else:
            print(f'Form is not valid: {form.errors}')
            return JsonResponse({'result': 'error', 'errors': form.errors, 'sell_form_html': render_to_string('sell_stock_form.html', {'sell_form': form}, request=request)})
    else:
        return redirect('stocks')  # Redirect to the 'stocks' page if the request is not an AJAX request


def stocks_view(request):
    stocks = Stock.objects.all()  # Get all Stock objects
    return render(request, './stocks.html', {'stocks': stocks})  # Render the stocks view

from django.shortcuts import render, redirect
from .forms import TradeForm
from .models import Trade, Portfolio

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


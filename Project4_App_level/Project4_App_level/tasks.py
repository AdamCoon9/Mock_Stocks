from alpha_vantage.timeseries import TimeSeries

from .models import stock

 

def update_stock_prices():

   ts = TimeSeries(key='1R3V8W52LXNUAN0G')

   for stock in stock.objects.all():

        data, _ = ts.get_quote(symbol=stock.symbol)

        stock.current_value = data['05. price']

        stock.save()
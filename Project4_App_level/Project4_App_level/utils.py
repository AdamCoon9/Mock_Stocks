import yfinance as yf
import matplotlib.pyplot as plt

def fetch_and_plot(symbol='AAPL', start_date='2016-01-01', end_date='2024-06-30'):
    # Get the data for the specified stock
    data = yf.download(symbol, start_date, end_date)

    # Generate the plot
    plt.figure(figsize=(10,5))
    plt.plot(data['Close'], label='Close')
    plt.plot(data['Open'], label='Open')
    plt.plot(data['High'], label='High')
    plt.plot(data['Low'], label='Low')
    plt.title(f'{symbol} Stock Data')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

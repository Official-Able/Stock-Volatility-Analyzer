#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import yfinance as yf
import numpy as np

# Define the list of stock symbols
stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NFLX', 'FB', 'NVDA', 'INTC', 'AMD']

# Function to calculate volatility
def calculate_volatility(prices):
    returns = prices.pct_change().dropna()
    volatility = np.std(returns) * np.sqrt(252)  # 252 trading days in a year
    return volatility

# Function to advise the client based on volatility
def advise_client(volatility):
    if volatility < 0.2:
        return "Low volatility: Consider for conservative investment."
    elif 0.2 <= volatility < 0.4:
        return "Moderate volatility: Suitable for balanced investment."
    elif volatility >= 0.4:
        return "High volatility: Recommended for aggressive investment with caution."
    else:
        return "Insufficient data to advise."

# Fetch stock data and calculate volatility
print("Stock\t\tVolatility\t\tAdvice")
print("-" * 50)
for symbol in stock_symbols:
    try:
        stock_data = yf.download(symbol, start="2023-01-01", end="2024-01-01", progress=False)
        stock_close_prices = stock_data['Close']
        volatility = calculate_volatility(stock_close_prices)
        advice = advise_client(volatility)
        print(f"{symbol}\t\t{volatility:.4f}\t\t{advice}")
    except Exception as e:
        print(f"{symbol}\t\tNaN\t\tError: {e}")


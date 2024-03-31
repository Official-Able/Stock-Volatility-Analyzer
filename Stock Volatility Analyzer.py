#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime

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

# Function to validate date format
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Prompt user for number of stocks to consider
while True:
    num_stocks = int(input("How many stocks do you want to consider? "))
    confirm = input(f"Confirm you want to consider {num_stocks} stocks? (yes/no) ")
    if confirm.lower() == 'yes':
        break
    elif confirm.lower() == 'no':
        continue
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

# Gather stock symbols and date range from the user
stock_symbols = []
while True:
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    if not is_valid_date(start_date):
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        continue
    else:
        break

while True:
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    if not is_valid_date(end_date):
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        continue
    else:
        break

# Dictionary to store stock data DataFrames
stock_data_dict = {}

for i in range(num_stocks):
    while True:
        stock_symbol = input(f"Enter the ticker symbol for stock {i+1}: ").upper()
        confirm = input(f"Confirm stock symbol '{stock_symbol}'. Is it correct? (yes/no) ")
        if confirm.lower() == 'yes':
            # Fetch stock data from Yahoo Finance
            try:
                stock_data = yf.download(stock_symbol, start=start_date, end=end_date, progress=False)
                stock_data_dict[stock_symbol] = stock_data
                stock_symbols.append(stock_symbol)
                break
            except Exception as e:
                print(f"Error fetching data for {stock_symbol}: {e}")
                continue
        elif confirm.lower() == 'no':
            continue
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

# Print confirmation message
print("Stock data has been fetched successfully.")

# Extract closing prices and calculate volatility
print("Stock\t\tVolatility\t\tAdvice")
print("-" * 50)
for symbol in stock_symbols:
    try:
        # Extract closing prices from the DataFrame
        stock_close_prices = stock_data_dict[symbol]['Close']
        # Calculate volatility
        volatility = calculate_volatility(stock_close_prices)
        # Provide advice based on volatility
        advice = advise_client(volatility)
        # Print results
        print(f"{symbol}\t\t{volatility:.4f}\t\t{advice}")
    except Exception as e:
        print(f"{symbol}\t\tNaN\t\tError: {e}")

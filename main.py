import os
from dotenv import load_dotenv
from decimal import Decimal, getcontext
from tabulate import tabulate
import diskcache as dc
from market_price import get_market_price  # Import the function from the new module

# Set precision for Decimal operations
getcontext().prec = 10

# Load the .env file
load_dotenv()

# Get environment variables
total_funds = Decimal(os.getenv('TOTAL_FUNDS', '0'))
cache_ttl = int(os.getenv('CACHE_TTL', '3600'))  # Cache TTL in seconds
stock_price_increase_ratio = Decimal(os.getenv('STOCK_PRICE_INCREASE_RATIO', '1.03'))  # Stock price increase ratio

# Define the Swensen model categories and read their funds needed from the .env file
swensen_model = [
    {'id': 'DME', 'name': 'Domestic Equity', 'funds_needed': Decimal(os.getenv('DME_FUNDS', '0'))},
    {'id': 'FRE', 'name': 'Foreign Equity', 'funds_needed': Decimal(os.getenv('FRE_FUNDS', '0'))},
    {'id': 'EME', 'name': 'Emerging Markets Equity', 'funds_needed': Decimal(os.getenv('EME_FUNDS', '0'))},
    {'id': 'TRE', 'name': 'Real Estate', 'funds_needed': Decimal(os.getenv('TRE_FUNDS', '0'))},
    {'id': 'TBI', 'name': 'Bonds', 'funds_needed': Decimal(os.getenv('TBI_FUNDS', '0'))},
    {'id': 'PEQ', 'name': 'Private Equity', 'funds_needed': Decimal(os.getenv('PEQ_FUNDS', '0'))}
]

# Calculate the total funds needed
total_funds_needed = sum(category['funds_needed'] for category in swensen_model)

# Create a table for the Swensen model categories
swensen_table = [
    [category['id'], category['name'], f"${category['funds_needed']:.2f}"]
    for category in swensen_model
]

# Print the total funds available and total funds needed
print("Funds Summary:")
print(tabulate([['Total funds available', f"${total_funds:.2f}"], ['Total funds needed', f"${total_funds_needed:.2f}"]], headers=["Description", "Amount"]))

# Check if the total funds needed matches the total funds available
if total_funds == total_funds_needed:
    print("\nThe total funds needed match the total funds available.")
else:
    difference = total_funds - total_funds_needed
    print("\nThe total funds needed do not match the total funds available.")
    print(tabulate([['Total funds available', f"${total_funds:.2f}"], ['Total funds needed', f"${total_funds_needed:.2f}"], ['Difference', f"${difference:.2f}"]], headers=["Description", "Amount"]))

# Define the stock tickers and read their values from the .env file
stock_tickers = {
    'EME': os.getenv('TICKER_EME', ''),
    'FRE': os.getenv('TICKER_FRE', ''),
    'TRE': os.getenv('TICKER_TRE', ''),
    'DME': os.getenv('TICKER_DME', ''),
    'PEQ': os.getenv('TICKER_PEQ', ''),
    'TBI': os.getenv('TICKER_TBI', '')
}

# Create a cache object in the .cache folder
cache = dc.Cache('.cache')

# Create a data structure to hold ticker symbols and their corresponding categories
ticker_data = []
total_investment_value = Decimal('0')
for category in swensen_model:
    ticker_symbol = stock_tickers.get(category['id'])
    # Check cache first
    if ticker_symbol in cache:
        current_market_price = Decimal(cache[ticker_symbol])
    else:
        # If not in cache, fetch the current market price and store it in cache
        current_market_price = get_market_price(ticker_symbol)
        if current_market_price is not None:
            cache.set(ticker_symbol, str(current_market_price), expire=cache_ttl)  # Cache for TTL seconds

    if current_market_price is not None:
        # Calculate adjusted price with the increase ratio
        adjusted_price = current_market_price * stock_price_increase_ratio
        # Calculate number of shares to buy
        shares_to_buy = (category['funds_needed'] // adjusted_price).quantize(Decimal('1.'))
        # Calculate the investment value
        investment_value = shares_to_buy * current_market_price
        # Calculate the delta between investment value and original fund value
        delta = investment_value - category['funds_needed']

        ticker_data.append({
            'category_id': category['id'],
            'category_name': category['name'],
            'ticker_symbol': ticker_symbol,
            'current_market_price': current_market_price,
            'adjusted_price': adjusted_price,
            'shares_to_buy': shares_to_buy,
            'investment_value': investment_value,
            'original_fund_value': category['funds_needed'],
            'delta': delta
        })

        # Add to total investment value
        total_investment_value += investment_value

# Close the cache when done
cache.close()

# Create a table for the stock ticker data
ticker_table = [
    [ticker['category_id'], ticker['category_name'], ticker['ticker_symbol'], f"${ticker['current_market_price']:.2f}", f"${ticker['adjusted_price']:.2f}", ticker['shares_to_buy'], f"${ticker['investment_value']:.2f}", f"${ticker['original_fund_value']:.2f}", f"${ticker['delta']:.2f}"]
    for ticker in ticker_data if ticker['current_market_price'] is not None
]

# Print the Swensen model categories table
print("\nSwensen Model Categories:")
print(tabulate(swensen_table, headers=["Category ID", "Category Name", "Funds Needed"]))

# Print the stock ticker data table
print("\nStock Ticker Data:")
print(tabulate(ticker_table, headers=["Category ID", "Category Name", "Ticker Symbol", "Current Market Price", "Adjusted Price (Increase Ratio)", "Shares to Buy", "Investment Value", "Original Fund Value", "Delta"]))

# Calculate the remainder
remainder = total_funds - total_investment_value

# Print the total investment value and remainder
print("\nInvestment Summary:")
print(tabulate([['Total Investment Value', f"${total_investment_value:.2f}"], ['Remainder vs Total Funds', f"${remainder:.2f}"]], headers=["Description", "Amount"]))

# Show a warning if the remainder is negative
if remainder < 0:
    print("\nWarning: The total investment value exceeds the total funds available!")

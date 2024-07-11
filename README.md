# Investment Allocation Script

## Overview

This script helps allocate investment funds across different categories based on the Swensen model. It retrieves the current market prices of specified stock tickers, calculates the number of shares to buy for each category, and provides an investment summary. If a stock price is higher than the allocated funds for a category, the script will skip that category and instruct the user to update the environment configuration for the next run.

## Goals

- Allocate investment funds according to the Swensen model.
- Retrieve current market prices for specified stock tickers.
- Calculate the number of shares to buy for each category.
- Provide an investment summary and remainder of funds.
- Handle cases where stock prices are higher than allocated funds by instructing the user to update the configuration.

## Outputs

- Total funds available.
- Investment summary for each category, including:
  - Category ID and name.
  - Ticker symbol.
  - Current market price.
  - Adjusted price (including a specified increase ratio).
  - Number of shares to buy.
  - Investment value.
  - Original allocated funds.
  - Delta (difference between investment value and original funds).
- Remainder of funds.
- Instructions for updating the configuration if any categories were skipped due to high stock prices.

## Instructions

### Prerequisites

- Python 3.9 or later.
- Virtual environment (venv) setup.

### Setup

1. Clone the repository or download the script files.
2. Set up a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file in the root directory of the project by copying the contents of the `.env.sample` file:
   ```sh
   cp .env.sample .env
   ```
2. Fill in the `.env` file with the required values. You can obtain an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and set it in the `.env` file.

### Example `.env` File

```plaintext
# Allocated funds for each category
DME_FUNDS=3000.00
FRE_FUNDS=1500.00
EME_FUNDS=1000.00
TRE_FUNDS=2000.00
TBI_FUNDS=1500.00
PEQ_FUNDS=1000.00

# Tickers
TICKER_DME=VTI
TICKER_FRE=VEA
TICKER_EME=VWO
TICKER_TRE=VNQ
TICKER_TBI=VGIT
TICKER_PEQ=VTIP

# Categories to process (comma-separated list of category IDs, e.g., "DME,FRE")
CATEGORIES_TO_PROCESS=

# Other settings
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
CACHE_TTL=3600  # Cache Time-To-Live in seconds
STOCK_PRICE_INCREASE_RATIO=1.03  # Stock price increase ratio (e.g., 1.03 for a 3% increase)
```

### Running the Script

To run the script, use the following command:

```sh
python main.py
```

### Updating the Configuration

If any categories are skipped due to high stock prices, the script will output instructions to update the `.env` file. Update the `CATEGORIES_TO_PROCESS` variable with the IDs of the skipped categories for the next run.

For example, if the `TRE` category was skipped, update the `.env` file as follows:

```plaintext
CATEGORIES_TO_PROCESS=TRE
```

Then, run the script again to process the skipped categories.

### Example Output

```
Funds Summary:
------------------------------
| Description       | Amount   |
------------------------------
| Total funds available | $10000.00 |

Swensen Model Categories:
------------------------------
| Category ID | Category Name       | Funds Needed |
------------------------------
| DME         | Domestic Equity     | $3000.00     |
| FRE         | Foreign Equity      | $1500.00     |
| EME         | Emerging Markets    | $1000.00     |
| TRE         | Real Estate         | $2000.00     |
| TBI         | Bonds               | $1500.00     |
| PEQ         | Private Equity      | $1000.00     |

Stock Ticker Data:
------------------------------------------------------------------------------------------
| Category ID | Category Name       | Ticker Symbol | Current Market Price | Adjusted Price | Shares to Buy | Investment Value | Original Fund Value | Delta |
------------------------------------------------------------------------------------------
| DME         | Domestic Equity     | VTI           | $200.00               | $206.00        | 14            | $2800.00          | $3000.00            | -$200.00 |
| FRE         | Foreign Equity      | VEA           | $50.00                | $51.50         | 29            | $1450.00          | $1500.00            | -$50.00  |
| EME         | Emerging Markets    | VWO           | $40.00                | $41.20         | 24            | $960.00           | $1000.00            | -$40.00  |
| TRE         | Real Estate         | VNQ           | $90.00                | $92.70         | 21            | $1890.00          | $2000.00            | -$110.00 |
| TBI         | Bonds               | VGIT          | $60.00                | $61.80         | 24            | $1440.00          | $1500.00            | -$60.00  |
| PEQ         | Private Equity      | VTIP          | $30.00                | $30.90         | 32            | $960.00           | $1000.00            | -$40.00  |

Investment Summary:
-----------------------------------------
| Description           | Amount         |
-----------------------------------------
| Total Investment Value | $9500.00       |
| Remainder vs Total Funds | $500.00      |

Warning: The total investment value exceeds the total funds available!

The following categories were skipped due to high stock prices:
 - TRE

Please update the .env file with the categories to process next time.
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
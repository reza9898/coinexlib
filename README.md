# CoinexLib

`CoinexLib` is a Python library for interacting with the CoinEx API. This library simplifies the process of accessing CoinEx's cryptocurrency trading features, allowing developers to retrieve market data, manage balances, and place orders.

---

## Features
- **Market Data Retrieval**: Fetch market depth, recent trades, candlestick data, and futures market information.
- **Account Management**: Access spot and futures account balances.
- **Order Management**: Place, check the status of, and manage orders in spot and futures markets.
- **Futures Management**: Adjust position leverage and retrieve current positions.

---

## Installation

Install the library using pip:

```bash
pip install coinexlib
```

---

## Usage

### Initialize the API
To use `CoinexLib`, you need an API key and secret from CoinEx. Initialize the API client as follows:

```python
from coinexlib import CoinexAPI

api = CoinexAPI("your_access_id", "your_secret_key")
```

### Fetch Spot Market Depth
Retrieve the market depth for a specific spot market:

```python
market_depth = api.get_market_depth("BTCUSDT", limit=10, interval="0")
print(market_depth)
```

### Retrieve Account Balance
Get your account balance for spot trading:

```python
balance = api.get_balance()
print(balance)
```

### Place a Futures Order
Place a buy or sell order in the futures market:

```python
order = api.place_order_futures(
    market="BTCUSDT",
    market_type="FUTURES",
    side="buy",
    order_type="limit",
    amount="0.1",
    price="20000"
)
print(order)
```

### Retrieve Futures Positions
Get the current futures positions:

```python
positions = api.get_current_position("BTCUSDT")
print(positions)
```

---

## Methods

### Market Data
- **`get_market_depth(market, limit, interval)`**: Retrieve spot market depth.
- **`get_market_depth_futures(market, limit, interval)`**: Retrieve futures market depth.
- **`get_market_deals(market, limit, last_id)`**: Fetch recent spot market trades.
- **`get_market_candlesticks_futures(market, limit, period, price_type)`**: Retrieve futures market candlestick data.

### Account Management
- **`get_balance()`**: Get spot account balance.
- **`get_balance_futures()`**: Get futures account balance.

### Order Management
- **`place_order_futures(market, market_type, side, order_type, amount, price, client_id, is_hide, stp_mode)`**: Place a futures order.
- **`order_status_futures(market, order_id)`**: Check the status of a futures order.
- **`adjust_position_leverage(market, market_type, margin_mode, leverage)`**: Adjust leverage for a market position.

---

## Requirements
- Python 3.6+
- `requests` library

Install requirements with:

```bash
pip install requests
```

---

## License
This project is licensed under the MIT License.

---

## Support
If you encounter issues or have questions, please open an issue on the [GitHub repository](https://github.com/reza9898/coinexlib).

---

## Disclaimer
This library is a third-party implementation and is not affiliated with or endorsed by CoinEx. Use at your own risk.

# CoinexLib

**Version: 1.1.0**

`CoinexLib` is a Python library for interacting with the CoinEx API. This library simplifies the process of accessing CoinEx's cryptocurrency trading features, allowing developers to retrieve market data, manage balances, and place orders.

---

## Features
- **Market Data Retrieval**: Fetch market depth, recent trades, candlestick data, and futures market information.
- **Account Management**: Access spot and futures account balances.
- **Order Management**: Place, check the status of, and manage orders in spot and futures markets.
- **Futures Management**: Adjust position leverage and retrieve current positions.
- **User Transaction Records**: Retrieve transactions for specific user orders.
- **Order Placement**: Place single and batch orders, including stop orders.

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

### Place a Spot Order
Place a buy or sell order in the spot market:

```python
order = api.place_order(
    market="BTCUSDT",
    market_type="SPOT",
    side="buy",
    order_type="limit",
    amount="0.1",
    price="25000"
)
print(order)
```

### Place a Stop Order
Place a buy or sell stop order in the spot market:

```python
order = api.place_stop_order(
    market="BTCUSDT",
    market_type="SPOT",
    side="buy",
    order_type="limit",
    amount="0.1",
    price="25000"
)
print(order)
```

### Batch Place Orders
Place multiple orders in batch:

```python 
orders = [
    {"market": "BTCUSDT", "market_type": "SPOT", "side": "buy", "order_type": "limit", "amount": "0.1", "price": "25000"},
    {"market": "ETHUSDT", "market_type": "SPOT", "side": "sell", "order_type": "limit", "amount": "1", "price": "1800"}
]
batch_order = api.batch_place_orders(orders)
print(batch_order)
``` 
### Query Order Status
Query the status of a specific order:

```python 
order_status = api.query_order_status(market="BTCUSDT", order_id=123456789)
print(order_status)
```

### Retrieve Futures Positions
Get the current futures positions:

```python
positions = api.get_current_position("BTCUSDT")
print(positions)
```
---
## New Methods Added in Version 1.1.0

### Market Data
- **`get_market_status(market)`**: Retrieve the market status for specified markets or all markets. 
- **`get_market_transactions(market, limit, last_id)`**: Retrieve recent transaction records for a specific market.
- **`get_market_index(market)`**: Retrieve the market index information for specified markets or all markets.

### User Transactions
- **`get_user_transactions(market, market_type, side, start_time, end_time, page, limit)`**: Retrieve user transaction records for a specific market. 
- **`get_user_order_transactions(market, market_type, order_id, page, limit)`**: Retrieve transaction records for a specific user order.

### Order Management
- **`place_order(market, market_type, side, order_type, amount, price, ccy, client_id, is_hide, stp_mode)`**: Place an order in the spot or margin market.
- **`place_stop_order(market, market_type, side, order_type, amount, trigger_price, price, ccy, client_id, is_hide, stp_mode)`**: Place a stop order in the spot or margin market.
- **`batch_place_orders(orders)`**: Place multiple orders in batch.
- **`batch_place_stop_orders(orders)`**: Place multiple stop orders in batch.
- **`query_order_status(market, order_id)`**: Query the status of a specific order.

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
This library is a third-party implementation and is not affiliated with or endorsed by Coinex. Use at your own risk.

import time
import datetime
import requests
import hmac
import hashlib
import json


class Utils(): 
    def timestamp_to_strdatetime(timestamp: int) -> str:
        """
        Converts a timestamp to a string in the format '%Y%m%d %H:%M:%S'.
    
        :param timestamp: The timestamp to be converted (in seconds).
        :return: A string representing the date and time in the specified format.
        """
        # Convert timestamp to datetime object
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        
        # Format the datetime object to a string
        formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        
        return formatted_date

class CoinexAPI:
    """
    A class for interacting with the CoinEx API, providing methods for 
    retrieving market data, managing balances, and placing orders.
    """
    BASE_URL = "https://api.coinex.com"

    def __init__(self, access_id, secret_key):
        """
        Initializes the CoinexAPI client with the required credentials.

        :param access_id: The access ID for API authentication.
        :param secret_key: The secret key for API authentication.
        """
        self.access_id = access_id
        self.secret_key = secret_key

    def _get_timestamp(self):
        """Get the current timestamp in milliseconds."""
        return str(int(time.time() * 1000))

    def _generate_signature(self, method, request_path, body=None):
        """
        Generate an HMAC-SHA256 signature for API requests.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param request_path: The API endpoint path.
        :param body: (Optional) The request body as a dictionary.
        :return: A tuple containing the signature and the timestamp.
        """
        timestamp = self._get_timestamp()
        body_str = json.dumps(body) if body else ''
        prepared_str = f"{method}{request_path}{body_str}{timestamp}"
        #print(prepared_str)
        signed_str = hmac.new(
            bytes(self.secret_key, 'latin-1'),
            msg=bytes(prepared_str, 'latin-1'),
            digestmod=hashlib.sha256
        ).hexdigest().lower()
        return signed_str, timestamp

    def _make_request(self, method, endpoint, params=None, data=None):
        """
        Make an authenticated HTTP request to the CoinEx API.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param endpoint: The API endpoint path.
        :param params: (Optional) Query parameters as a dictionary.
        :param data: (Optional) Request body as a dictionary.
        :return: The API response as a JSON dictionary.
        """
        method = method.upper()
        request_path = f"/v2{endpoint}"
        if params:
            query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
            request_path += f"?{query_string}"

            
        signed_str, timestamp = self._generate_signature(method, request_path, data)
        headers = {
            'X-COINEX-KEY': self.access_id,
            'X-COINEX-SIGN': signed_str,
            'X-COINEX-TIMESTAMP': timestamp,
            "Content-Type": "application/json; charset=utf-8",
        }

        url = f"{self.BASE_URL}{request_path}"
        response = requests.request(method, url, headers=headers, json=data)
        return response.json()

    def get_market_depth(self, market, limit, interval) -> dict:
        """
        Retrieve the depth of the spot market.

        :param market: The market name (e.g., 'BTCUSDT').
        :param limit: Number of depth entries to retrieve.
        :param interval: Interval for depth data.
        :return: Market depth data as a dictionary.
        """
        params = {
            "market": market,
            "limit": limit,
            "interval": interval
        }
        return self._make_request("GET", "/spot/depth", params=params)

    def get_market_depth_futures(self, market, limit, interval) -> dict:
        """
        Retrieve the depth of the futures market.

        :param market: The market name (e.g., 'BTCUSDT').
        :param limit: Number of depth entries to retrieve.
        :param interval: Interval for depth data.
        :return: Futures market depth data as a dictionary.
        """
        params = {
            "market": market,
            "limit": limit,
            "interval": interval
        }
        return self._make_request("GET", "/futures/depth", params=params)

    def get_market_deals(self, market, limit = 100, last_id = 0) -> dict:
        """
        Retrieve recent spot market deals.

        :param market: The market name (e.g., 'BTCUSDT').
        :param limit: Maximum number of deals to retrieve (default: 100).
        :param last_id: The ID of the last deal to start retrieving from (default: 0).
        :return: Market deals data as a dictionary.
        """
        params = {
            "market": market,
            "limit": limit,
            "last_id": last_id
        }
        return self._make_request("GET", "/spot/deals", params=params)
    def get_market_deals_futures(self, market, limit = 100, last_id = 0) -> dict:
        """
        Retrieve recent Future market deals.

        :param market: The market name (e.g., 'BTCUSDT').
        :param limit: Maximum number of deals to retrieve (default: 100).
        :param last_id: The ID of the last deal to start retrieving from (default: 0).
        :return: Market deals data as a dictionary.
        """
        params = {
            "market": market,
            "limit": limit,
            "last_id": last_id
        }
        return self._make_request("GET", "/futures/deals", params=params)

    def get_market_candlesticks(self, market, limit, period) -> dict:
        """
        Retrieve candlestick data for a spot market.

        :param market: The market name (e.g., 'BTCUSDT').
        :param limit: Number of candlestick entries to retrieve.
        :param period: Time period for candlesticks (e.g., "1min", "5min", "15min", "1hour", "4hour", "1day", "1week").
        :return: Candlestick data as a dictionary.
        """
        params = {
            "market": market,
            "limit": limit,
            "period": period
        }
        return self._make_request("GET", "/spot/kline", params=params)

    def get_market_candlesticks_futures(self, market, limit, period, price_type = "latest_price") -> dict:
        """
        Retrieve candlestick data for a futures market.

        :param market: The market name (e.g., 'BTCUSDT').
        :param limit: Number of candlestick entries to retrieve.
        :param period: Time period for candlesticks (e.g., "1min", "5min", "15min", "1hour", "4hour", "1day", "1week").
        :param price_type: Price type (default: 'latest_price').
        :return: Candlestick data as a dictionary.
        """
        params = {
            "market": market,
            "price_type": price_type,
            "limit": limit,
            "period": period
        }
        return self._make_request("GET", "/futures/kline", params=params)
        
    def get_market_information_futures(self, market) -> dict:
        """
        Retrieve information about a futures market.

        :param market: The market name (e.g., 'BTCUSDT').
        :return: Market information data as a dictionary.
        """
        params = {
            "market": market,
        }
        return self._make_request("GET", "/futures/ticker", params=params)

    def get_balance(self) -> dict:
        """
        Retrieve the spot account balance.

        :return: Account balance data as a dictionary.
        """
        return self._make_request("GET", "/assets/spot/balance")

    def get_balance_futures(self) -> dict:
        """
        Retrieve the futures account balance.

        :return: Account balance data as a dictionary.
        """
        return self._make_request("GET", "/assets/futures/balance")

    def adjust_position_leverage(self, market, market_type, margin_mode, leverage) -> dict: 
        """
        Adjust the leverage for a given market position.

        :param market: The market name (e.g., 'BTCUSDT').
        :param market_type: The type of market (e.g., 'FUTURES').
        :param margin_mode: The margin mode (e.g., 'cross' or 'isolated').
        :param leverage: The leverage value to set.
        :return: Response data as a dictionary.
        """
        data = {
            "market" : market,
            "market_type" : market_type,
            "margin_mode" : margin_mode,
            "leverage" : leverage
        }
        return self._make_request("POST", "/futures/adjust-position-leverage", data=data)

    def get_current_position(self, market, market_type= "FUTURES", page = 1, limit= 100) -> dict: 
        """
        Retrieve the current position for a given market.

        :param market: The market name (e.g., 'BTCUSDT').
        :param market_type: The type of market (default: 'FUTURES').
        :param page: Page number for paginated results (default: 1).
        :param limit: Number of positions to retrieve per page (default: 100).
        :return: Current position data as a dictionary.
        """
        params = {
            "market" : market,
            "market_type" : market_type,
            "page" : page,
            "limit" : limit
        }
        return self._make_request("GET", "/futures/pending-position", params= params)

    def place_order_futures(self, market: str, market_type: str, side: str, order_type: str, amount: str, price: str = None, client_id: str = None,
    is_hide: bool = False, stp_mode: str = None) -> dict:
        """
        Place a futures order on the CoinEx platform.
        :param market: Market name, e.g., "CETUSDT".
        :param market_type: Market type, e.g., "FUTURES".
        :param side: Order side, e.g., "buy" or "sell".
        :param order_type: Order type, e.g., "limit" or "market".
        :param amount: Order amount as a string.
        :param price: (Optional) Order price for limit orders.
        :param client_id: (Optional) User-defined client ID for the order.
        :param is_hide: (Optional) Whether to hide the order from public depth information. Default is False.
        :param stp_mode: (Optional) Self-trading protection mode, e.g., "ct", "cm", or "both".
        :return: JSON response containing the order details.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "side": side,
            "type": order_type,
            "amount": amount,
            "is_hide": is_hide,
        }
        if price is not None:
            data["price"] = price
        if client_id is not None:
            data["client_id"] = client_id
        if stp_mode is not None:
            data["stp_mode"] = stp_mode
    
        return self._make_request("POST", "/futures/order", data=data)

    def order_status_futures(self, market, order_id) -> dict: 
        """
        Retrieve the status of a futures order.

        :param market: The market name (e.g., 'BTCUSDT').
        :param order_id: The unique identifier of the order.
        :return: Order status data as a dictionary.
        """
        params = {
            "market" : market,
            "order_id" : order_id,
        }
        return self._make_request("GET", "/futures/order-status", params= params)

    def close_position_futures(self,market: str,market_type: str,order_type: str,price: str = None,amount: str = None,client_id: str = None,
                       is_hide: bool = False, stp_mode: str = None ) -> dict:
        """
        Close a position in the futures market.
    
        :param market: Market name, e.g., "CETUSDT".
        :param market_type: Market type, e.g., "FUTURES".
        :param order_type: Order type, e.g., "limit" or "market".
        :param price: (Optional) Order price, required for limit orders.
        :param amount: (Optional) Order amount. Null to close all positions.
        :param client_id: (Optional) User-defined client ID for the order.
        :param is_hide: (Optional) Whether to hide the order from public depth information. Default is False.
        :param stp_mode: (Optional) Self-trading protection mode, e.g., "ct", "cm", or "both".
        :return: JSON response containing the order details.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "type": order_type,
            "is_hide": is_hide,
        }
        if price is not None:
            data["price"] = price
        if amount is not None:
            data["amount"] = amount
        if client_id is not None:
            data["client_id"] = client_id
        if stp_mode is not None:
            data["stp_mode"] = stp_mode
    
        return self._make_request("POST", "/futures/close-position", data=data)
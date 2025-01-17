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

    def _get_timestamp(self) -> str:
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

    def get_market_status(self, market: str = "") -> dict:
        """
        Retrieve the market status for specified markets or all markets.
    
        :param market: (Optional) Comma-separated list of market names. Leave empty to query all markets.
                       Example: "BTCUSDT,ETHUSDT".
        :return: JSON response containing market status data.
        """
        params = {"market": market} if market else {}
        return self._make_request("GET", "/spot/market", params=params)

    def get_market_transactions(self, market: str, limit: int = 100, last_id: int = 0) -> dict:
        """
        Retrieve recent transaction records for a specific market.
    
        :param market: Market name. Example: "BTCUSDT".
        :param limit: (Optional) Number of transaction records to retrieve. Default is 100. Max is 1000.
        :param last_id: (Optional) Starting TxID for the query. Use 0 to start from the latest record.
        :return: JSON response containing transaction records.
        """
        params = {
            "market": market,
            "limit": limit,
            "last_id": last_id
        }
        return self._make_request("GET", "/spot/deals", params=params)

    def get_market_index(self, market: str = "") -> dict:
        """
        Retrieve the market index information for specified markets or all markets.
    
        :param market: (Optional) Comma-separated list of market names. Leave empty to query all markets.
                       Example: "BTCUSDT,ETHUSDT".
        :return: JSON response containing market index data.
        """
        params = {"market": market} if market else {}
        return self._make_request("GET", "/spot/index", params=params)

    def get_user_transactions(self, market: str, market_type: str, side: str = None, start_time: int = None, end_time: int = None, 
        page: int = 1, limit: int = 10) -> dict:
        """
        Retrieve user transaction records for a specific market.
    
        :param market: Market name. Example: "BTCUSDT".
        :param market_type: Market type. Example: "SPOT" or "MARGIN".
        :param side: (Optional) Order side, e.g., "buy" or "sell". Null to return both sides.
        :param start_time: (Optional) Query start time in milliseconds.
        :param end_time: (Optional) Query end time in milliseconds.
        :param page: (Optional) Page number for pagination. Default is 1.
        :param limit: (Optional) Number of records per page. Default is 10.
        :return: JSON response containing user transaction data.
        """
        params = {
            "market": market,
            "market_type": market_type,
            "page": page,
            "limit": limit,
        }
        if side:
            params["side"] = side
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
    
        return self._make_request("GET", "/spot/user-deals", params=params)

    def get_user_order_transactions(self, market: str, market_type: str, order_id: int, page: int = 1, limit: int = 10) -> dict:
        """
        Retrieve transaction records for a specific user order.
    
        :param market: Market name. Example: "BTCUSDT".
        :param market_type: Market type. Example: "SPOT" or "MARGIN" or "FUTURES".
        :param order_id: Order ID for the transaction.
        :param page: (Optional) Page number for pagination. Default is 1.
        :param limit: (Optional) Number of records per page. Default is 10.
        :return: JSON response containing user order transaction data.
        """
        params = {
            "market": market,
            "market_type": market_type,
            "order_id": order_id,
            "page": page,
            "limit": limit,
        }
        return self._make_request("GET", "/spot/order-deals", params=params)


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

    def get_market_information(self, market: str = "") -> dict:
        """
        Retrieve market information, including the latest price, high/low prices, volume, etc.
    
        :param market: (Optional) Comma-separated list of market names. Leave empty to query all markets.
                       Example: "LATUSDT,ELONUSDT".
        :return: JSON response containing market information.
        """
        params = {"market": market} if market else {}
        return self._make_request("GET", "/spot/ticker", params=params)
        
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

    def place_order(self, market: str, market_type: str, side: str, order_type: str, amount: str, price: str = None,ccy: str = None,
                    client_id: str = None, is_hide: bool = False, stp_mode: str = None,) -> dict:
        """
        Place an order in the spot or margin market.
    
        :param market: Market name, e.g., "CETUSDT".
        :param market_type: Market type, e.g., "SPOT" or "MARGIN".
        :param side: Order side, e.g., "buy" or "sell".
        :param order_type: Order type, e.g., "limit" or "market".
        :param amount: Order amount as a string.
        :param price: (Optional) Order price for limit orders.
        :param ccy: (Optional) Currency name for market orders. Can only be base or quote currency.
        :param client_id: (Optional) User-defined ID for the order.
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
        if ccy is not None:
            data["ccy"] = ccy
        if client_id is not None:
            data["client_id"] = client_id
        if stp_mode is not None:
            data["stp_mode"] = stp_mode
    
        return self._make_request("POST", "/spot/order", data=data)

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

    def place_stop_order(self,market: str, market_type: str, side: str, order_type: str, amount: str, trigger_price: str, price: str = None,
        ccy: str = None, client_id: str = None, is_hide: bool = False, stp_mode: str = None,) -> dict:
        """
        Place a stop order in the spot or margin market.
    
        :param market: Market name, e.g., "CETUSDT".
        :param market_type: Market type, e.g., "SPOT" or "MARGIN".
        :param side: Order side, e.g., "buy" or "sell".
        :param order_type: Order type, e.g., "limit" or "market".
        :param amount: Order amount as a string.
        :param trigger_price: Stop order trigger price.
        :param price: (Optional) Order price for limit orders.
        :param ccy: (Optional) Currency name for market orders. Can only be base or quote currency.
        :param client_id: (Optional) User-defined ID for the stop order.
        :param is_hide: (Optional) Whether to hide the order from public depth information. Default is False.
        :param stp_mode: (Optional) Self-trading protection mode, e.g., "ct", "cm", or "both".
        :return: JSON response containing the stop order ID.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "side": side,
            "type": order_type,
            "amount": amount,
            "trigger_price": trigger_price,
            "is_hide": is_hide,
        }
        if price is not None:
            data["price"] = price
        if ccy is not None:
            data["ccy"] = ccy
        if client_id is not None:
            data["client_id"] = client_id
        if stp_mode is not None:
            data["stp_mode"] = stp_mode
    
        return self._make_request("POST", "/spot/stop-order", data=data)

    def batch_place_orders(self, orders: list) -> dict:
        """
        Place multiple orders in batch.
    
        :param orders: A list of dictionaries, where each dictionary represents an order.
        :return: JSON response containing the batch order details.
        """
        data = {
            "orders": orders
        }
    
        return self._make_request("POST", "/spot/batch-order", data=data)

    def batch_place_stop_orders(self, orders: list) -> dict:
        """
        Place multiple stop orders in batch.
    
        :param orders: A list of dictionaries, where each dictionary represents a stop order.
        :return: JSON response containing the batch stop order details.
        """
        data = {
            "orders": orders
        }
    
        return self._make_request("POST", "/spot/batch-stop-order", data=data)

    def query_order_status(self, market: str, order_id: int) -> dict:
        """
        Query the status of a specific order.
    
        :param market: The market name (e.g., "CETUSDT").
        :param order_id: The unique ID of the order.
        :return: JSON response containing the order details.
        """
        params = {
            "market": market,
            "order_id": order_id
        }
        return self._make_request("GET", "/spot/order-status", params=params)

    def query_order_status_futures(self, market, order_id) -> dict: 
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

    def batch_query_order_status(self, market: str, order_ids: str) -> dict:
        """
        Query the status of multiple orders in batch.
    
        :param market: The market name (e.g., "CETUSDT").
        :param order_ids: A string containing order IDs separated by commas (e.g., "13400,13401").
        :return: JSON response containing the order details for each order ID.
        """
        params = {
            "market": market,
            "order_ids": order_ids
        }
        return self._make_request("GET", "/spot/batch-order-status", params=params)

    def get_unfilled_order(self, market_type: str, market: str = None, side: str = None, client_id: str = None, page: int = 1, limit: int = 10) -> dict:
        """
        Fetch unfilled orders based on specified parameters.
    
        :param market: (Optional) The market name (e.g., "CETUSDT"). Pass None to return orders in all markets.
        :param market_type: The market type ("SPOT", "MARGIN").
        :param side: (Optional) The order side ("buy" or "sell"). Pass None to return orders of both sides.
        :param client_id: (Optional) User-defined ID.
        :param page: (Optional) The page number for pagination (default is 1).
        :param limit: (Optional) The number of results per page (default is 10).
        :return: JSON response containing the unfilled order details.
        """
        params = {
            "market_type": market_type,
            "page": page,
            "limit": limit
        }
        if market is not None : 
            params["market"] = market
        if side is not None: 
            params["side"] = side
        if client_id is not None : 
            params["client_id"] = client_id
            
        return self._make_request("GET", "/spot/pending-order", params=params)

    def get_filled_order(self, market_type: str, market: str = None, side: str = None, page: int = 1, limit: int = 10) -> dict:
        """
        Fetch filled orders based on specified parameters.
    
        :param market: (Optional) The market name (e.g., "CETUSDT"). Pass None to return orders from all markets.
        :param market_type: The market type ("SPOT", "MARGIN").
        :param side: (Optional) The order side ("buy" or "sell"). Pass None to return orders of both sides.
        :param page: (Optional) The page number for pagination (default is 1).
        :param limit: (Optional) The number of results per page (default is 10).
        :return: JSON response containing the filled order details.
        """
        params = {
            "market_type": market_type,
            "page": page,
            "limit": limit
        }
        if market is not None : 
            params["market"] = market
        if side is not None: 
            params["side"] = side
        return self._make_request("GET", "/spot/finished-order", params=params)

    def get_unfilled_stop_order(self, market_type: str, market: str = None, side: str = None, page: int = 1, limit: int = 10) -> dict:
        """
        Fetch unfilled stop orders based on specified parameters.
    
        :param market: (Optional) The market name (e.g., "CETUSDT"). Pass None to return orders from all markets.
        :param market_type: The market type ("SPOT", "MARGIN").
        :param side: (Optional) The order side ("buy" or "sell"). Pass None to return orders of both sides.
        :param page: (Optional) The page number for pagination (default is 1).
        :param limit: (Optional) The number of results per page (default is 10).
        :return: JSON response containing the unfilled stop order details.
        """
        params = {
            "market_type": market_type,
            "page": page,
            "limit": limit
        }

        if market is not None : 
            params["market"] = market
        if side is not None: 
            params["side"] = side
        return self._make_request("GET", "/spot/pending-stop-order", params=params)

    def modify_order(self, market: str, market_type: str, order_id: int, amount: str = None, price: str = None) -> dict:
        """
        Modify an existing order with new amount or price.
    
        :param market: The market name (e.g., "CETUSDT").
        :param market_type: The market type ("SPOT", "MARGIN").
        :param order_id: The ID of the order to modify.
        :param amount: (Optional) The new amount for the order.
        :param price: (Optional) The new price for the order.
        :return: JSON response containing the modified order details.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "order_id": order_id,
        }

        if amount is not None : 
            data["amount"] = amount
        if price is not None: 
            data["price"] = price
        return self._make_request("POST", "/spot/modify-order", data=data)

    def modify_stop_order(self, market: str, market_type: str, stop_id: int, amount: str = None, price: str = None, trigger_price: str = None) -> dict:
        """
        Modify an existing stop order with new amount, price, or trigger price.
        This will cancel the old stop order and create a new one.
    
        :param market: The market name (e.g., "CETUSDT").
        :param market_type: The market type ("SPOT", "MARGIN", or "FUTURES").
        :param stop_id: The ID of the stop order to modify.
        :param amount: (Optional) The new amount for the stop order.
        :param price: (Optional) The new price for the stop order.
        :param trigger_price: (Optional) The new trigger price for the stop order.
        :return: JSON response containing the modified stop order details.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "stop_id": stop_id,
        }
        if amount is not None : 
            data["amount"] = amount
        if price is not None: 
            data["price"] = price
        if trigger_price is not None: 
            data["trigger_price"] = trigger_price
        return self._make_request("POST", "/spot/modify-stop-order", data=data)

    def cancel_all_orders(self, market: str, market_type: str, side: str = None) -> dict:
        """
        Cancel all orders in a specified market. Optionally filter by order side (buy/sell).
        
        :param market: The market name (e.g., "CETUSDT").
        :param market_type: The market type ("SPOT", "MARGIN").
        :param side: (Optional) The order side ("buy" or "sell"). If not provided, all orders will be canceled.
        :return: JSON response indicating success or failure.
        """
        data = {
            "market": market,
            "market_type": market_type,
        }
        if side is not None: 
            data["side"] = side
        return self._make_request("POST", "/spot/cancel-all-order", data=data)

    def cancel_order(self, market: str, market_type: str, order_id: int) -> dict:
        """
        Cancel a specific order in a specified market.
        
        :param market: The market name (e.g., "CETUSDT").
        :param market_type: The market type ("SPOT", "MARGIN").
        :param order_id: The ID of the order to cancel.
        :return: JSON response indicating success or failure.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "order_id": order_id
        }
        return self._make_request("POST", "/spot/cancel-order", data=data)

    def cancel_stop_order(self, market: str, market_type: str, stop_id: int) -> dict:
        """
        Cancel a specific stop order in a specified market.
        
        :param market: The market name (e.g., "CETUSDT").
        :param market_type: The market type ("SPOT", "MARGIN").
        :param stop_id: The ID of the stop order to cancel.
        :return: JSON response indicating success or failure.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "stop_id": stop_id
        }
        return self._make_request("POST", "/spot/cancel-stop-order", data=data)

    def cancel_batch_orders(self, market: str, order_ids: list) -> dict:
        """
        Cancel multiple orders in a specified market.
        
        :param market: The market name (e.g., "CETUSDT").
        :param order_ids: A list of order IDs to cancel.
        :return: JSON response indicating success or failure.
        """
        data = {
            "market": market,
            "order_ids": order_ids
        }
        return self._make_request("POST", "/spot/cancel-batch-order", data=data)

    def cancel_batch_stop_orders(self, market: str, stop_ids: list) -> dict:
        """
        Cancel multiple stop orders in a specified market.
        
        :param market: The market name (e.g., "CETUSDT").
        :param stop_ids: A list of stop order IDs to cancel.
        :return: JSON response indicating success or failure.
        """
        data = {
            "market": market,
            "stop_ids": stop_ids
        }
        return self._make_request("POST", "/spot/cancel-batch-stop-order", data=data)

    def cancel_order_by_client_id(self, market: str, market_type: str, client_id: str) -> dict:
        """
        Cancel an order using a user-defined client ID in a specified market and market type.
        
        :param market: The market name (e.g., "CETUSDT").
        :param market_type: The type of market (e.g., "MARGIN").
        :param client_id: The user-defined client ID for the order to be canceled.
        :return: JSON response indicating success or failure.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "client_id": client_id
        }
        return self._make_request("POST", "/spot/cancel-order-by-client-id", data=data)

    def cancel_stop_order_by_client_id(self, market: str, market_type: str, client_id: str) -> dict:
        """
        Cancel a stop order using a user-defined client ID in a specified market and market type.
        
        :param market: The market name (e.g., "CETUSDT").
        :param market_type: The type of market ("SPOT, "MARGIN").
        :param client_id: The user-defined client ID associated with the stop order to be canceled.
        :return: JSON response indicating success or failure.
        """
        data = {
            "market": market,
            "market_type": market_type,
            "client_id": client_id
        }
        return self._make_request("POST", "/spot/cancel-stop-order-by-client-id", data=data)

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
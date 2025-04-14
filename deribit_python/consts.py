from enum import Enum, StrEnum

"""
Constants used throughout the Deribit API wrapper.
"""

# API URLs
TESTNET_BASE_URL = "https://test.deribit.com/api/v2"
MAINNET_BASE_URL = "https://www.deribit.com/api/v2"


class DeribitMethod(StrEnum):
    """
    Deribit API method names.
    """
    # Public methods
    GET_INSTRUMENTS = "/public/get_instruments"
    GET_ORDER_BOOK = "public/get_order_book"
    GET_TICKER = "public/ticker"
    GET_BOOK_SUMMARY_BY_CURRENCY="public/get_book_summary_by_currency"

    GET_INSTRUMENT_INFO = "public/get_instrument_info"
    GET_INSTRUMENT_EXCHANGE_RATE = "public/get_instrument_exchange_rate"
    GET_TIME = "public/get_time"
    GET_CURRENCIES = "public/get_currencies"
    GET_LAST_TRADES = "public/get_last_trades"
    GET_SUMMARY = "public/get_summary"
    GET_ANNOUNCEMENTS = "public/get_announcements"
    GET_BOOK_SUMMARY = "public/get_book_summary"
    GET_DELIVERY_PRICES = "public/get_delivery_prices"
    GET_FUNDING_CHART_DATA = "public/get_funding_chart_data"
    GET_HISTORICAL_VOLATILITY = "public/get_historical_volatility"
    GET_INDEX = "public/get_index"
    GET_TRADINGVIEW_CHART_DATA = "public/get_tradingview_chart_data"
    
    # Private methods
    GET_ACCOUNT_SUMMARY = "private/get_account_summary"
    GET_POSITIONS = "private/get_positions"
    GET_OPEN_ORDERS = "private/get_open_orders"
    GET_ORDER_STATE = "private/get_order_state"
    GET_ORDER_HISTORY = "private/get_order_history"
    GET_TRADE_HISTORY = "private/get_trade_history"
    GET_USER_TRADES = "private/get_user_trades"
    GET_DEPOSITS = "private/get_deposits"
    GET_WITHDRAWALS = "private/get_withdrawals"
    GET_TRANSFERS = "private/get_transfers"
    GET_SUBACCOUNTS = "private/get_subaccounts"
    GET_SUBACCOUNT_BALANCES = "private/get_subaccount_balances"
    GET_MARGIN_FOR_POSITION = "private/get_margin_for_position"
    GET_LIQUIDATION_PRICE = "private/get_liquidation_price"
    GET_ESTIMATED_MARGIN = "private/get_estimated_margin"
    GET_SETTLEMENT_HISTORY = "private/get_settlement_history"
    GET_TRANSACTION_LOG = "private/get_transaction_log"
    GET_NOTIFICATIONS = "private/get_notifications"
    GET_PORTFOLIO_MARGINS = "private/get_portfolio_margins"
    GET_POSITION = "private/get_position"
    GET_POSITION_HISTORY = "private/get_position_history"
    GET_RISK_LIMITS = "private/get_risk_limits"
    GET_STOP_ORDER_HISTORY = "private/get_stop_order_history"
    GET_USER_TRADES_BY_CURRENCY = "private/get_user_trades_by_currency"
    GET_USER_TRADES_BY_INSTRUMENT = "private/get_user_trades_by_instrument"
    GET_USER_TRADES_BY_ORDER = "private/get_user_trades_by_order"
    GET_WITHDRAWAL_PRIORITIES = "private/get_withdrawal_priorities"
    GET_WITHDRAWAL_WHITELIST = "private/get_withdrawal_whitelist"
    
    # Trading methods
    BUY = "private/buy"
    SELL = "private/sell"
    CLOSE_POSITION = "private/close_position"
    CANCEL = "private/cancel"
    CANCEL_ALL = "private/cancel_all"
    CANCEL_ALL_BY_CURRENCY = "private/cancel_all_by_currency"
    CANCEL_ALL_BY_INSTRUMENT = "private/cancel_all_by_instrument"
    CANCEL_BY_LABEL = "private/cancel_by_label"
    EDIT = "private/edit"
    
    # Authentication methods
    AUTH = "public/auth"
    LOGOUT = "private/logout"
    DISABLE_HEARTBEAT = "private/disable_heartbeat"
    ENABLE_HEARTBEAT = "private/enable_heartbeat"
    SET_HEARTBEAT = "public/set_heartbeat"
    TEST = "public/test"
    

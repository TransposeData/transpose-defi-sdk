import pandas as pd

from transpose.sql.ohlcv import ohlcv_query


class Chart:
    """
    The Chart class provides a simple interface for generating OHLCV charts of generic token
    prices across multiple chains.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes a new Chart object.

        :param api_key: The Tranpose API key.
        """

        self.api_key = api_key


    def ohlcv(self, chain: str, token_address: str, from_timestamp: str, to_timestamp: str, timeframe: str) -> pd.DataFrame:
        """
        Returns OHLCV data for a given token address, time range, and timeframe.

        :param chain: The chain to query.
        :param token_address: The token address to query.
        :param from_timestamp: The start of the time range to query.
        :param to_timestamp: The end of the time range to query.
        :param timeframe: The timeframe to query.
        :return: The OHLCV data.
        """

        

import plotly.graph_objects as go
from typing import Optional
import pandas as pd

from transpose.sql.ohlc import ohlc_query
from transpose.sql.token import token_metadata_query
from transpose.sql.general import latest_block_query
from transpose.utils.request import send_transpose_sql_request
from transpose.utils.exceptions import ChartingError
from transpose.utils.address import to_checksum_address
from transpose.utils.time import to_iso


class Chart:
    """
    The Chart class provides a simple interface for generating OHLC charts of generic token
    prices across multiple chains.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes a new Chart object.

        :param api_key: The Tranpose API key.
        """

        self.api_key = api_key

        # validate API key
        if api_key is None or not isinstance(api_key, str) or len(api_key) <= 0: 
            raise ChartingError('Transpose API key is required')
        self.api_key = api_key
        
        # run test query
        send_transpose_sql_request(
            api_key=self.api_key,
            query=latest_block_query('ethereum')
        )


    def ohlc(self, chain: str, token_address: str, from_timestamp: str, to_timestamp: str, timeframe: str,
             return_raw_data: bool=False) -> Optional[pd.DataFrame]:

        """
        Returns OHLC data for a given token address, time range, and timeframe. To return the raw
        DataFrame instead of charting the OHLC data, set return_raw_data to True.

        :param chain: The chain to query.
        :param token_address: The token address to query.
        :param from_timestamp: The start of the time range to query.
        :param to_timestamp: The end of the time range to query.
        :param timeframe: The timeframe to query.
        :param return_raw_data: Whether to return the raw DataFrame instead of charting the OHLC data.
        :return: The OHLC data as a DataFrame if return_raw_data is True, otherwise None.
        """

        # validate chain
        if chain not in ['ethereum', 'goerli', 'polygon']:
            raise ChartingError('Invalid chain')
        
        # validate token address
        token_address = to_checksum_address(token_address)
        if token_address is None: raise ChartingError('Invalid token address')

        # validate timestamps
        try: from_timestamp = to_iso(from_timestamp)
        except Exception as e: raise ChartingError('Invalid from timestamp') from e
        try: to_timestamp = to_iso(to_timestamp)
        except Exception as e: raise ChartingError('Invalid to timestamp') from e

        # validate timeframe
        if timeframe not in ['day', 'hour', 'minute']:
            raise ChartingError('Invalid timeframe')

        # submit token metadata query request
        query = token_metadata_query(chain, token_address)
        token_metadata = send_transpose_sql_request(self.api_key, query)[0]

        # submit OHLC query request
        query = ohlc_query(chain, token_address, from_timestamp, to_timestamp, timeframe)
        raw_ohlc_data = send_transpose_sql_request(self.api_key, query)
        if len(raw_ohlc_data) == 0: raise ChartingError('No OHLC data found')
    
        # parse data
        ohlc_df = pd.DataFrame([{
            'timestamp': row['t'], 'open': row['o'], 'high': row['h'], 'low': row['l'], 'close': row['c']} 
            for row in raw_ohlc_data
        ])

        # configure dataframe
        ohlc_df.set_index('timestamp', inplace=True)
        ohlc_df.index = pd.to_datetime(ohlc_df.index)

        # return raw data
        if return_raw_data: 
            return ohlc_df

        # chart data
        token_name = token_metadata['name'] or token_metadata['symbol'] or token_address
        token_symbol = token_metadata['symbol'] or token_address
        fig = go.Figure(go.Ohlc(x=ohlc_df.index, open=ohlc_df['open'], high=ohlc_df['high'], low=ohlc_df['low'], close=ohlc_df['close']))
        fig.update_layout(
            title=f'{token_name} Price Chart',
            yaxis_title=f'{token_symbol} Price (USD)',
            xaxis_title='Datetime (UTC)'
        )

        # display chart
        fig.show()
def ohlc_query(chain: str, token_address: str, from_timestamp: str, to_timestmap: str, timeframe: str) -> str:
    """
    Returns a SQL query that returns OHLC data for a given token address, time range, and timeframe.

    :param chain: The chain to query.
    :param token_address: The token address to query.
    :param from_timestamp: The start of the time range to query.
    :param to_timestamp: The end of the time range to query.
    :param timeframe: The timeframe to query.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT 
            
            agg._date AS t, 
            max.price AS o,
            agg._high AS h, 
            agg._low AS l,
            min.price AS c

        FROM
        
            (SELECT 
                date_trunc('{timeframe}', timestamp) AS _date,
                MIN(price) as _low,
                MAX(price) as _high,
                MIN(block_number) as lbn,
                MAX(block_number) as gbn
            FROM {chain}.token_prices
            WHERE token_address = '{token_address}'
            AND timestamp >= '{from_timestamp}'
            AND timestamp <= '{to_timestmap}'
            GROUP BY _date) AS agg

            JOIN {chain}.token_prices AS max
            ON token_address = '{token_address}'
            AND block_number = agg.lbn
            
            JOIN {chain}.token_prices AS min
            ON min.token_address = '{token_address}'
            AND min.block_number = agg.gbn

        ORDER BY _date ASC;
        """
def token_metadata_query(chain: str, token_address: str) -> str:
    """
    Returns a SQL query that returns token metadata for a given token address.

    :param chain: The chain to query.
    :param token_address: The token address to query.
    :return: The SQL query.
    """

    return \
        f"""
        SELECT name, symbol, decimals
        FROM {chain}.tokens
        WHERE contract_address = '{token_address}';
        """
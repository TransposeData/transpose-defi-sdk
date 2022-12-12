# transpose-financial-analysis-sdk

The Transpose Financial Analysis SDK is a simple Python package for charting generic token prices and performing similar financial analysis of on-chain data. At the moment, the only supported functionality is the ability to download or chart OHLC data for any token address on Ethereum, Goerli, and Polygon.

The underlying price data is sourced for every token on the supported networks, regardless of centralized listing status, volume, or liquidity. This data is derived from DEX data across over 24 different DEXs, including Uniswap, Sushiswap, Balancer, and Curve, and nearly 200k DEX pools. The token prices are always normalized to accurate USD prices using Chainlink price feeds. The full list of supported DEXs can be in the [docs](https://docs.transpose.io/sql/tables/protocol-layer/dex-swaps/smoothyswap_dex_swaps/).

## Installation

To install the package, run the following command in your Python environment:

```bash
pip install transpose-financial-analysis-sdk
```

## Retrieving an API key

To use the SDK, you will need an API key for Transpose. You can sign up for a free API key by visting the [Transpose App](https://app.transpose.io). If you have any questions on getting started, feature requests, or contributing to the SDK, please reach out to us on [Discord](http://discord.gg/transpose).

## Getting Started

### Charting OHLC prices

OHLC stands for open-high-low-close and is a common way to represent price data over fixed time intervals. For example, a chart of hourly OHLC prices for a token would show the open, high, low, and close prices for each hour.

To start charting data, simply import and instantiate the `Chart` class from the SDK and call its `ohlc` method.

```python
from transpose.chart import Chart

# initialize Chart with your API key
chart = Chart(api_key='enP9LfNUmGt0WRg1LNG4nSYK2MC1waEH')

# chart OHLC data for a token
chart.ohlc(
    chain='ethereum', 
    token_address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', # token address for WETH
    from_timestamp='2021-01-01', 
    to_timestamp='2021-02-01', 
    timeframe='hour'
)
```

The above code will generate a chart of hourly OHLC prices for WETH from January 1st, 2021 to February 1st, 2021. The address for WETH could be replaced with any valid token address on the supported chains.

By default, Plotly will automatically render the chart in your browser. If you would like to save the chart as a HTML file, you can pass the `save_as` parameter to the `ohlc` method:

```python
chart.ohlc(
    chain='ethereum', 
    token_address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 
    from_timestamp='2021-01-01', 
    to_timestamp='2021-02-01', 
    timeframe='hour',
    save_as='test.html'
)
```

### Downloading OHLC data

To return the data directly as a Pandas DataFrame, you can pass the `return_df` parameter to the `ohlc` method:

```python
price_df = chart.ohlc(
    chain='ethereum', 
    token_address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 
    from_timestamp='2021-01-01', 
    to_timestamp='2021-02-01', 
    timeframe='hour',
    return_df=True
)
```

The `price_df` DataFrame will contain a timestamp column and four price columns: `open`, `high`, `low`, and `close`.

### Charting Options

The `ohlc` method accepts a number of optional parameters to customize the chart. The following parameters are available:

- `chain`: The blockchain network to query. Supported values are `ethereum`, `goerli`, and `polygon`.
- `token_address`: The address of the token to chart.
- `from_timestamp`: The start date for the chart. This can be a string in the format `YYYY-MM-DD` or a Unix timestamp.
- `to_timestamp`: The end date for the chart. This can be a string in the format `YYYY-MM-DD` or a Unix timestamp.
- `timeframe`: The time interval to chart. Supported values are `minute`, `hour`, and `day`.

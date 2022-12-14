from transpose.chart import Chart


if __name__ == '__main__':
    chart = Chart('YOUR API KEY')
    chart.ohlc(
        chain='ethereum', 
        token_address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 
        from_timestamp='2021-01-01', 
        to_timestamp='2021-02-01', 
        timeframe='hour',
        save_as='test.html'
    )
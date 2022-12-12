from transpose.chart import Chart


if __name__ == '__main__':
    chart = Chart('enP9LfNUmGt0WRg1LNG4nSYK2MC1waEH')
    raw_data = chart.ohlc('ethereum', '0x6b175474e89094c44da98b954eedeac495271d0f', '2021-01-01', '2021-02-01', 'day')
    print(raw_data)
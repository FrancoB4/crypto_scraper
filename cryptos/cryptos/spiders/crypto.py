import scrapy
import datetime
# coin = //a[@class="tv-screener__symbol"]/text()
CRYPTO_NAMES = '//a[@class="tv-screener__symbol"]/text()'
# all numeric data = //td[@class="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big"]/text()
CRYPTO_DATA = '//td[@class="tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big"]/text()'


class CryptoSpider(scrapy.Spider):
    name = 'crypto'
    start_urls = [
        'https://es.tradingview.com/markets/cryptocurrencies/prices-all/'
    ]
    custom_settings = {
        'FEEDS': {
            f'{datetime.date.today().strftime("%H-%d-%m-%Y")}.csv' :{
                'format': 'csv',
                'encoding': 'utf-8',
                'indent': 4,
                'overwrite': True
            }
        },
        'MEMUSAGE_LIMIT_MB': 2048,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }


    def parse(self, response):
        coins = response.xpath(CRYPTO_NAMES).getall()
        data = response.xpath(CRYPTO_DATA).getall()
        data = list(filter(lambda x: x != '0.00%', data))
        mkt_cap = []
        fd_mkt_cap = []
        price = []
        avail_coins = []
        total_coins = []
        traded_volume = []
        for coin in coins:
            mkt_cap.append(data[0])
            data.pop(0)
            fd_mkt_cap.append(data[0])
            data.pop(0)
            price.append(data[0])
            data.pop(0)
            avail_coins.append(data[0])
            data.pop(0)
            total_coins.append(data[0])
            data.pop(0)
            traded_volume.append(data[0])
            data.pop(0)

        for i, coin in enumerate(coins):
            yield {
                'coin': coin,
                'market cap': mkt_cap[i],
                'fd market cap': fd_mkt_cap[i],
                'price': price[i],
                'avail coins': avail_coins[i],
                'total coins': total_coins[i],
                'traded volume': traded_volume[i]
            }
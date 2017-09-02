from discord.ext import commands
from coinmarketcap import Market
import datetime

format_currency_props = [
    "price_usd",
    "24h_volume_usd",
    "market_cap_usd",
    "available_supply",
    "total_supply",
    "24h_volume_cash"
]


class CoinMarketException(Exception):
    '''Exception class for CoinMarket'''


class CoinMarket:

    def __init__(self, bot):
        '''
        Initiates CoinMarket

        @param bot - discord bot object
        '''
        self.bot = bot
        self.market = Market()

    def _fetch_currency_data(self, currency, fiat):
        '''
        Fetches the currency data based on the desired currency

        @param currency - the cryptocurrency to search for (i.e. 'bitcoin', 'ethereum')
        @param fiat - desired currency (i.e. 'EUR', 'USD')
        @return - currency data
        '''
        return self.market.ticker(currency, convert=fiat)

    def _format_currency_data(self, currency, fiat):
        '''
        Formats the data fetched

        @param currency - the cryptocurrency to search for (i.e. 'bitcoin', 'ethereum')
        @param fiat - desired currency (i.e. 'EUR', 'USD')
        @return - formatted currency data
        '''
        data = self._fetch_currency_data(currency, fiat)
        formatted_data = ''
        for json in data:
            for prop in json:
                if prop != 'id':
                    if prop in format_currency_props:
                        formatted_data += "{}: {:,}\n".format(prop, float(json[prop]))
                    elif prop == "last_updated":
                        converted_time = datetime.datetime.fromtimestamp(int(json[prop]))
                        formatted_data += "{}: {}\n".format(prop, converted_time.strftime('%Y-%m-%d %H:%M:%S'))
                        formatted_data += "(Time may vary depending on the timezone you're in)\n"
                    else:
                        formatted_data += "{}: {}\n".format(prop, json[prop])

        return formatted_data

    @commands.command(name='search', description='Displays the data of the specified currency.')
    async def display_currency(self, currency: str, fiat=''):
        '''
        Obtains the data of the specified currency and displays them.

        @param currency - the cryptocurrency to search for (i.e. 'bitcoin', 'ethereum')
        @param fiat - desired currency (i.e. 'EUR', 'USD')
        '''
        try:
            data = self._format_currency_data(currency, fiat)
            await self.bot.say(data)
        except:
            await self.bot.say("Failed to find the specified currency.")
            raise CoinMarketException("Failed to find the specified currency.")

    def _fetch_coinmarket_stats(self):
        '''
        Fetches the coinmarket stats

        @return - market stats
        '''
        return self.market.stats()

    def _format_coinmarket_stats(self):
        '''
        Formats coinmarket stats

        @return - formatted stats
        '''
        stats = self._fetch_coinmarket_stats()
        formatted_stats = ''
        for stat in stats:
            formatted_stats += "{}: {:,}\n".format(stat, stats[stat])

        return formatted_stats

    @commands.command(name='stats', description='Displays the market stats.')
    async def display_stats(self):
        '''
        Displays the market stats
        '''
        try:
            stats = self._format_coinmarket_stats()
            await self.bot.say(stats)
        except:
            await self.bot.say("Failed to gather coinmarket stats.")
            raise CoinMarketException("Failed to gather coinmarket stats.")


def setup(bot):
    bot.add_cog(CoinMarket(bot))

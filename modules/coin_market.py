from coinmarketcap import Market


class CoinMarketException(Exception):
    """Exception class for CoinMarket"""


class CoinMarket:
    """
    Handles CoinMarketCap API features
    """
    def __init__(self):
        """
        Initiates CoinMarket

        @param bot - discord bot object
        """
        self.market = Market()

    def _fetch_currency_data(self, currency, fiat):
        """
        Fetches the currency data based on the desired currency

        @param currency - the cryptocurrency to search for (i.e. 'bitcoin', 'ethereum')
        @param fiat - desired currency (i.e. 'EUR', 'USD')
        @return - currency data
        """
        return self.market.ticker(currency, convert=fiat)

    def _format_currency_data(self, data, currency, fiat):
        """
        Formats the data fetched

        @param currency - the cryptocurrency to search for (i.e. 'bitcoin', 'ethereum')
        @param fiat - desired currency (i.e. 'EUR', 'USD')
        @return - formatted currency data
        """
        try:
            isPositivePercent = True
            formatted_data = ''
            for obj in data:
                hour_trend = ''
                if float(obj['percent_change_1h']) >= 0:
                    hour_trend = ':arrow_upper_right:'
                else:
                    hour_trend = ':arrow_lower_right:'
                    isPositivePercent = False

                formatted_data += '__**#{}. {} ({})**__ {}\n'.format(obj['rank'], obj['name'], obj['symbol'], hour_trend)
                formatted_data += 'Price (USD): **${:,}**\n'.format(float(obj['price_usd']))
                if (obj['market_cap_usd'] is None):
                    formatted_data += 'Market Cap (USD): Unknown\n'
                else:
                    formatted_data += 'Market Cap (USD): **${:,}**\n'.format(float(obj['market_cap_usd']))
                if (obj['available_supply'] is None):
                    formatted_data += 'Available Supply: Unknown\n'
                else:
                    formatted_data += 'Available Supply: **{:,}**\n'.format(float(obj['available_supply']))
                formatted_data += 'Percent Change (1H): **{}%**\n'.format(obj['percent_change_1h'])
                formatted_data += 'Percent Change (24H): **{}%**\n'.format(obj['percent_change_24h'])
                formatted_data += 'Percent Change (7D): **{}%**\n'.format(obj['percent_change_7d'])

            return formatted_data, isPositivePercent
        except Exception as e:
            print("Failed to format data: " + e)

    async def get_currency(self, currency: str, fiat='USD'):
        """
        Obtains the data of the specified currency and returns them.

        @param currency - the cryptocurrency to search for (i.e. 'bitcoin', 'ethereum')
        @param fiat - desired currency (i.e. 'EUR', 'USD')
        """
        try:
            data = self._fetch_currency_data(currency, fiat)
            formatted_data, isPositivePercent = self._format_currency_data(data, currency, fiat)
        except Exception as e:
            formatted_data = "Unable to find the currency specified: " + currency
        return formatted_data, isPositivePercent

    def _fetch_coinmarket_stats(self):
        """
        Fetches the coinmarket stats

        @return - market stats
        """
        return self.market.stats()

    def _format_coinmarket_stats(self, stats):
        """
        Receives and formats coinmarket stats

        @return - formatted stats
        """
        try:
            formatted_stats = ''
            if (stats['total_market_cap_usd'] is None):
                formatted_stats += "Total Market Cap (USD): Unknown"
            else:
                formatted_stats += "Total Market Cap (USD): **${:,}**\n".format(float(stats['total_market_cap_usd']))

            formatted_stats += "Bitcoin Percentage of Market: **{:,}%**\n".format(stats['bitcoin_percentage_of_market_cap'])
            formatted_stats += "Active Markets: **{:,}**\n".format(stats['active_markets'])
            formatted_stats += "Active Currencies: **{:,}**\n".format(stats['active_currencies'])
            formatted_stats += "Active Assets: **{:,}**\n".format(stats['active_assets'])

            return formatted_stats
        except Exception as e:
            print("Failed to format data: " + e)

    async def get_stats(self):
        """
        Returns the market stats
        """
        try:
            stats = self._fetch_coinmarket_stats()
            formatted_stats = self._format_coinmarket_stats(stats)
            return formatted_stats
        except Exception as e:
            raise CoinMarketException(e)

    async def get_live_data(self, currency_list, fiat='USD'):
        """
        Returns updated info of coin stats

        @param currency_list - list of cryptocurrencies
        @param fiat - desired currency (i.e. 'EUR', 'USD')
        """
        try:
            formatted_data = ''
            for currency in currency_list:
                data = self._fetch_currency_data(currency, fiat)
                formatted_data += self._format_currency_data(data, currency, fiat)[0] + '\n'
            return formatted_data
        except Exception as e:
            raise CoinMarketException(e)

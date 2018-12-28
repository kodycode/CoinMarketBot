from bot_logger import logger
from coinmarketcap import Market
from currency_converter import CurrencyConverter
from requests.exceptions import RequestException

fiat_currencies = {
    'AUD': '$', 'BRL': 'R$', 'CAD': '$', 'CHF': 'Fr.',
    'CLP': '$', 'CNY': '¥', 'CZK': 'Kc', 'DKK': 'kr',
    'EUR': '€', 'GBP': '£', 'HKD': 'HK$', 'HUF': 'Ft',
    'IDR': 'Rp ', 'ILS': '₪', 'INR': '₹', 'JPY': '¥‎',
    'KRW': '₩', 'MXN': '$', 'MYR': 'RM', 'NOK': 'kr',
    'NZD': '$', 'PHP': '₱', 'PKR': 'Rupees', 'PLN': 'zł',
    'RUB': '₽', 'SEK': 'kr', 'SGD': 'S$', 'THB': '฿',
    'TRY': '₺', 'TWD': 'NT$', 'ZAR': 'R ', 'USD': '$'
}

fiat_suffix = [
    'CZK', 'DKK', 'HUF',
    'NOK', 'PKR', 'RUB',
    'SEK'
]

ETHEREUM = "ethereum"
SMALL_GREEN_TRIANGLE = "<:small_green_triangle:396586561413578752>"
SMALL_RED_TRIANGLE = ":small_red_triangle_down:"


class CurrencyException(Exception):
    """Exception class for invalid currencies"""


class CoinMarketException(Exception):
    """Exception class for CoinMarket"""


class FiatException(Exception):
    """Exception class for invalid fiat"""


class MarketStatsException(Exception):
    """Exception class for invalid retrieval of market stats"""


class CoinMarket:
    """Handles CoinMarketCap API features"""

    def __init__(self, api_key):
        """
        Initiates CoinMarket
        """
        self.market = Market(api_key)

    def fiat_check(self, fiat):
        """
        Checks if fiat is valid. If invalid, raise FiatException error.

        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        @return - uppercase fiat
        """
        if fiat is not fiat.upper():
            fiat = fiat.upper()
        if fiat not in fiat_currencies:
            error_msg = "This fiat currency is not supported: `{}`".format(fiat)
            raise FiatException(error_msg)
        return fiat

    def format_price(self, price, fiat, symbol=True):
        """
        Formats price under the desired fiat

        @param price - price to format
        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        @param symbol - if True add currency symbol to fiat
                        if False symbol will not be added
        @return - formatted price under fiat
        """
        c = CurrencyConverter()
        ucase_fiat = fiat.upper()
        price = float(c.convert(float(price), "USD", fiat))
        if symbol:
            if ucase_fiat in fiat_suffix:
                formatted_fiat = "{:,.6f} {}".format(float(price),
                                                     fiat_currencies[ucase_fiat])
            else:
                formatted_fiat = "{}{:,.6f}".format(fiat_currencies[ucase_fiat],
                                                    float(price))
        else:
            formatted_fiat = str(price)
        formatted_fiat = formatted_fiat.rstrip('0')
        if formatted_fiat.endswith('.'):
            formatted_fiat = formatted_fiat.replace('.', '')
        return formatted_fiat

    def fetch_currency_data(self, fiat="USD"):
        """
        Fetches all cryptocurrency data

        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        @return - currency data
        """
        try:
            return self.market.listings(limit=5000, convert=fiat)
        except RequestException as e:
            logger.error("Failed to retrieve data - "
                         "Connection error: {}".format(str(e)))
            return None
        except Exception as e:
            raise CurrencyException("Failed to fetch all cryptocurrencies: `{}`".format(str(e)))

    def _format_currency_data(self, data, fiat, single_search=True):
        """
        Formats the data fetched

        @param currency - the cryptocurrency to search for (i.e. 'bitcoin',
                          'ethereum')
        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        @param single_search - separate more lines if True
        @return - formatted currency data
        """
        try:
            price = CurrencyConverter()
            isPositivePercent = True
            formatted_data = ''
            hour_trend = ''
            if data['quote']['USD']['percent_change_24h'] is not None:
                if float(data['quote']['USD']['percent_change_24h']) >= 0:
                    hour_trend = SMALL_GREEN_TRIANGLE
                else:
                    hour_trend = SMALL_RED_TRIANGLE
                    isPositivePercent = False
            header = "__**#{}. {} ({})**__ {}".format(data['cmc_rank'],
                                                      data['name'],
                                                      data['symbol'],
                                                      hour_trend)
            converted_price = float(price.convert(float(data['quote']['USD']['price']),
                                                  'USD',
                                                  fiat))
            converted_price = "{:,.6f}".format(converted_price).rstrip('0')
            if converted_price.endswith('.'):
                converted_price = converted_price.replace('.', '')
            # formatted_btc = '{:,.8f}'.format(float(data['price_btc'])).rstrip('0')
            # if formatted_btc.endswith('.'):
            #     formatted_btc = formatted_btc.replace('.', '')
            # eth_price = eth_price.rstrip('.')
            # if single_search:
            #     eth_price += '\n'
            if data['quote']['USD']['market_cap'] is None:
                formatted_market_cap = 'Unknown'
            else:
                converted_market_cap = price.convert(float(data['quote']['USD']['market_cap_usd']),
                                                     'USD',
                                                     fiat)
            if fiat in fiat_suffix:
                formatted_price = '**{} {}**'.format(converted_price,
                                                     fiat_currencies[fiat])
                if data['quote']['USD']['market_cap_usd'] is not None:
                    formatted_market_cap = '**{:,} {}**'.format(int(converted_market_cap),
                                                                fiat_currencies[fiat])
            else:
                formatted_price = '**{}{}**'.format(fiat_currencies[fiat],
                                                    converted_price)
                if data['quote']['USD']['market_cap_usd'] is not None:
                    formatted_market_cap = '**{}{:,}**'.format(fiat_currencies[fiat],
                                                               int(converted_market_cap))
            if (data['circulating_supply'] is None):
                circulating_supply = 'Unknown'
            else:
                circulating_supply = '**{:,}**'.format(int(float(data['circulating_supply'])))
            if single_search:
                circulating_supply += '\n'
            percent_change_1h = '**{}%**'.format(data['percent_change_1h'])
            percent_change_24h = '**{}%**'.format(data['percent_change_24h'])
            percent_change_7d = '**{}%**'.format(data['percent_change_7d'])
            formatted_data = ("{}\n"
                              "Price ({}): {}\n"
                              # "Price (BTC): **{}**\n"
                              # "Price (ETH): **{}**\n"
                              "Market Cap ({}): {}\n"
                              "Circulating Supply: {}\n"
                              "Percent Change (1H): {}\n"
                              "Percent Change (24H): {}\n"
                              "Percent Change (7D): {}\n"
                              "".format(header,
                                        fiat,
                                        formatted_price,
                                        # formatted_btc,
                                        # eth_price,
                                        fiat,
                                        formatted_market_cap,
                                        circulating_supply,
                                        percent_change_1h,
                                        percent_change_24h,
                                        percent_change_7d))
            return formatted_data, isPositivePercent
        except Exception as e:
            raise CoinMarketException("Failed to format data ({}): {}".format(data['name'],
                                                                              e))

    def get_current_currency(self, market_list, acronym_list, currency, fiat):
        """
        Obtains the data of the specified currency and returns them using
        the current updated market list

        @param market_list - list of entire crypto market
        @param acronym_list - list of cryptocurrency acronyms
        @param currency - the cryptocurrency to search for (i.e. 'bitcoin',
                          'ethereum')
        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        """
        try:
            isPositivePercent = False
            fiat = self.fiat_check(fiat)
            if currency.upper() in acronym_list:
                currency = acronym_list[currency.upper()]
                if "Duplicate" in currency:
                    return currency, isPositivePercent
            if currency not in market_list:
                raise CurrencyException("Invalid currency: `{}`".format(currency))
            data = market_list[currency]
            # eth_price = self.get_converted_coin_amt(market_list, currency, ETHEREUM, 1)
            formatted_data, isPositivePercent = self._format_currency_data(data, fiat)
            return formatted_data, isPositivePercent
        except CurrencyException as e:
            raise
        except FiatException as e:
            raise
        except Exception as e:
            raise CoinMarketException(e)

    def fetch_coinmarket_stats(self, fiat="USD"):
        """
        Fetches the coinmarket stats

        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        @return - market stats
        """
        try:
            return self.market.stats(convert=fiat)
        except RequestException as e:
            logger.error("Failed to retrieve data - "
                         "Connection error: {}".format(str(e)))
            return None
        except Exception as e:
            raise MarketStatsException("Unable to retrieve crypto market stats "
                                       "at this time.")

    def _format_coinmarket_stats(self, stats, fiat):
        """
        Receives and formats coinmarket stats

        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        @return - formatted stats
        """
        try:
            c = CurrencyConverter()
            formatted_stats = ''
            if stats['quote']['USD']['total_market_cap'] is None:
                formatted_stats += "Total Market Cap (USD): Unknown"
            else:
                converted_price = int(c.convert(float(stats['quote']['USD']['total_market_cap']), 'USD', fiat))
                if fiat in fiat_suffix:
                    formatted_stats += "Total Market Cap ({}): **{:,} {}**\n".format(fiat,
                                                                                     converted_price,
                                                                                     fiat_currencies[fiat])
                else:
                    formatted_stats += "Total Market Cap ({}): **{}{:,}**\n".format(fiat,
                                                                                    fiat_currencies[fiat],
                                                                                    converted_price)
            if stats['quote']['USD']['total_volume_24h'] is None:
                formatted_stats += "Total Volume 24h (USD): Unknown"
            else:
                converted_price = int(c.convert(float(stats['quote']['USD']['total_volume_24h']), 'USD', fiat))
                if fiat in fiat_suffix:
                    formatted_stats += "Total Volume 24h (USD): **{:,} {}**\n".format(fiat,
                                                                                      converted_price,
                                                                                      fiat_currencies[fiat])
                else:
                    formatted_stats += "Total Volume 24h (USD): **{}{:,}**\n".format(fiat,
                                                                                     fiat_currencies[fiat],
                                                                                     converted_price)
            formatted_stats += "Bitcoin Dominance: **{:,}%**\n".format(stats['btc_dominance'])
            formatted_stats += "Ethereum Dominance: **{:,}%**\n".format(stats['eth_dominance'])
            formatted_stats += "Active Exchanges: **{:,}**\n".format(stats['active_exchanges'])
            formatted_stats += "Active Currencies: **{:,}**\n".format(stats['active_cryptocurrencies'])
            return formatted_stats
        except Exception as e:
            raise CoinMarketException("Failed to format data: `{}`".format(e))

    def get_current_stats(self, market_stats, fiat):
        """
        Returns the market stats

        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        @return - formatted market stats
        """
        try:
            fiat = self.fiat_check(fiat)
            formatted_stats = self._format_coinmarket_stats(market_stats, fiat)
            return formatted_stats
        except FiatException as e:
            raise
        except MarketStatsException as e:
            raise
        except Exception as e:
            raise CoinMarketException(e)

    def get_current_multiple_currency(self, market_list, acronym_list, currency_list, fiat, cached_data=None):
        """
        Returns updated info of multiple coin stats using the current
        updated market list
        @param market_list - list of entire crypto market
        @param acronym_list - list of cryptocurrency acronyms
        @param cached_data - a cache of formatted cryptocurrency data
        @param currency_list - list of cryptocurrencies to retrieve
        @param fiat - desired fiat currency (i.e. 'EUR', 'USD')
        @return - list of formatted cryptocurrency data
        """
        try:
            formatted_data = []
            data_list = []
            result_msg = ''
            for currency in currency_list:
                try:
                    if acronym_list is not None:
                        if currency.upper() in acronym_list:
                            currency = acronym_list[currency.upper()]
                            if "Duplicate" in currency:
                                return [[currency]]
                        if market_list[currency] not in data_list:
                            data_list.append(market_list[currency])
                    else:
                        if market_list[currency] not in data_list:
                            data_list.append(market_list[currency])
                except Exception as e:
                    raise CurrencyException("Invalid currency: `{}`"
                                            "".format(currency))
            data_list.sort(key=lambda x: int(x['rank']))
            for data in data_list:
                # eth_price = self.get_converted_coin_amt(market_list,
                #                                         data['id'],
                #                                         ETHEREUM,
                #                                         1)
                if cached_data is None:
                    formatted_msg = self._format_currency_data(data,
                                                               # eth_price,
                                                               fiat,
                                                               False)[0]
                else:
                    if cached_data:
                        if fiat not in cached_data:
                            cached_data[fiat] = {}
                        if data['id'] not in cached_data[fiat]:
                            formatted_msg = self._format_currency_data(data,
                                                                       # eth_price,
                                                                       fiat,
                                                                       False)[0]
                            cached_data[fiat][data['id']] = formatted_msg
                        else:
                            formatted_msg = cached_data[fiat][data['id']]
                    else:
                        formatted_msg = self._format_currency_data(data,
                                                                   # eth_price,
                                                                   fiat,
                                                                   False)[0]
                        if fiat not in cached_data:
                            cached_data[fiat] = {}
                        if data['id'] not in cached_data[fiat]:
                            cached_data[fiat][data['id']] = formatted_msg
                if len(result_msg) + len(formatted_msg) < 2000:
                    result_msg += "{}\n".format(formatted_msg)
                else:
                    formatted_data.append(result_msg)
                    result_msg = formatted_msg
            formatted_data.append(result_msg)
            return formatted_data, cached_data
        except CurrencyException as e:
            raise
        except FiatException as e:
            raise
        except Exception as e:
            raise CoinMarketException(e)

    def get_converted_coin_amt(self, market_list, currency1, currency2, currency_amt):
        """
        Converts coin to coin based on btc price
        """
        try:
            price_btc1 = float(market_list[currency1]['price_btc'])
            price_btc2 = float(market_list[currency2]['price_btc'])
            btc_amt = float("{:.8f}".format(currency_amt * price_btc1))
            converted_amt = "{:.8f}".format(btc_amt/price_btc2).rstrip('0')
            return converted_amt
        except Exception as e:
            print("Failed to convert coin. See error.log.")
            logger.error("Exception: {}".format(str(e)))

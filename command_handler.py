from modules.coin_market import CoinMarket
import asyncio
import discord


class CmdHandler:
    """
    Processes commands sent from Discord
    """
    def __init__(self, config_data):
        self.coin_market_prefix = '$'
        self.coin_market_cmd_handler = CoinMarketCommand()
        self.config_data = config_data

    async def process_command(self, client, message):
        if message.content.startswith('$'):
            await self.coin_market_cmd_handler.process_command(self.config_data,
                                                               client,
                                                               message)


class CoinMarketCommand:
    """
    Handles all Coin Market Cap related commands
    """
    def __init__(self):
        self.coin_market = CoinMarket()
        self.live_on = False

    async def search(self, client, message):
        """
        Displays the data of the specified currency.

        @param client - bot client
        @param message - command received
        """
        param = message.content.split()
        data = ''
        if len(param) == 3:
            data = await self.coin_market.get_currency(param[1], param[2])
        elif len(param) == 2:
            data = await self.coin_market.get_currency(param[1])
        else:
            await client.send_message(message.channel,
                                      "Please enter a currency to search. A "
                                      "particular fiat is optional.")
        em = discord.Embed(title="Search results",
                           description=data,
                           colour=0x008000)
        await client.send_message(message.channel, embed=em)

    async def stats(self, client, message):
        """
        Displays the market stats.

        @param client - bot client
        @param message - command received
        """
        data = await self.coin_market.get_stats()
        em = discord.Embed(title="Market Stats",
                           description=data,
                           colour=0x008000)
        await client.send_message(message.channel, embed=em)

    async def live(self, currency_list, live_channel, timer, client, message):
        """
        Displays live updates of coin stats in n-second intervals

        @param currency_list - list of currencies
        @param live_channel - the channel to message in
        @param timer - time interval between live updates
        @param client - bot client
        @param message - command received
        """
        if not self.live_on:
            self.live_on = True
            param = message.content.split()
            data = ''
            while True:
                try:
                    await client.purge_from(client.get_channel(live_channel),
                                            limit=100)
                except:
                    pass
                if param == 2:
                    data = await self.coin_market.get_live_data(currency_list,
                                                                param[1])
                else:
                    data = await self.coin_market.get_live_data(currency_list)
                em = discord.Embed(title="Live Currency Update",
                                   description=data,
                                   colour=0x008000)
                await client.send_message(client.get_channel(live_channel),
                                          embed=em)
                await asyncio.sleep(float(timer))

    async def process_command(self, config_data, client, message):
        """
        Processes commands to use

        @param client - bot client
        @param message - command received
        """
        if message.content.startswith("$search"):
            await self.search(client, message)
        elif message.content.startswith("$stats"):
            await self.stats(client, message)
        elif message.content.startswith("$live"):
            await self.live(config_data['live_check_currency'],
                            config_data['live_channel'],
                            config_data['live_update_interval'],
                            client,
                            message)

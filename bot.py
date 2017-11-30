import discord
import json
from command_handler import CmdHandler

# Wrapping this at some point
client = discord.Client()
config_data = ''
with open('config.json') as config:
    config_data = json.load(config)
handle = CmdHandler(config_data)


class CoinMarketBotException(Exception):
    """Exception class for CoinMarketBot"""


class CoinMarketBot:
    """Initiates the Bot"""

    def __init__(self, config_data):
        client.run(config_data["token"])

    @client.event
    async def on_ready():
        print('CoinMarketDiscordBot is online.')

    @client.event
    async def on_message(message):
        if message.author != client.user:
            await handle.process_command(client, message)


def main():
    try:
        CoinMarketBot(config_data)
    except Exception as e:
        print(e)


main()

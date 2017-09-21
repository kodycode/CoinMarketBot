# CoinMarketDiscordBot
A Discord bot that reports data from https://coinmarketcap.com/

Created with the python ![CoinMarketCap API](https://github.com/mrsmn/coinmarketcap-api) wrapper.

Click ![here](https://discordapp.com/oauth2/authorize?&client_id=353373501274456065&scope=bot) to add the bot to your server.

## Installation:
1. Install necessary requirements using ```pip install -r requirements.txt```
2. Rename config_template.json to config.json
3. Enter your discord token inside the token variable in config.py
4. Run with ```python bot.py```


## Commands:
| Commands      | Output        |
| ------------- |:-------------:|
| $search [CryptoCurrency to search for here (i.e. bitcoin, ethereum)] [Currency to convert to (i.e. USD, EUR, etc.)] | Displays the data of the specified currency. |
| $stats | Displays the overall stats of the coin market |
| $help | Displays available commands and descriptions of them |


## TODO:

- ~~24h bot hosting~~
- Improve formatting of the results
- Secure code
- Live Updates

## Donations

Although not required at all, I wouldn't mind accepting donations.

```
BTC: 1LBmomuVG1S3RYzLM134MKLqLsgUi72JGA
LTC: LXW66ZPnpSwtFUyRxXhxetyCn26kqKhu6k
ETH: 0x19A221CF972823C95C057d12A96eBc657488bD97
```

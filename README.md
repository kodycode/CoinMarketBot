# CoinMarketCapDiscordBot
A Discord bot that reports data from https://coinmarketcap.com/

Created with the python ![CoinMarketCap API](https://github.com/mrsmn/coinmarketcap-api) wrapper.

## Installation:
1. Install necessary requirements using ```pip install -r requirements.txt```
2. Rename config_template.py to config.py
3. Enter your discord token inside the token variable in config.py
4. Run with ```python bot.py```


## Commands:
| Commands      | Output        |
| ------------- |:-------------:|
| $search [CryptoCurrency to search for here (i.e. bitcoin, ethereum)] [Currency to convert to (i.e. USD, EUR, etc.)] | Displays the data of the specified currency. |
| $stats | Displays the overall stats of the coin market |
| $help | Displays available commands and descriptions of them |


## TODO:

- 24h bot hosting
- Improve formatting of the results
- Secure code

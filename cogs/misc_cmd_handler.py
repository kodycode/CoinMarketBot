from bot_logger import logger
from discord.ext import commands


class MiscCommands:
    """
    Handles misc commands
    """
    def __init__(self, bot):
        self.cmd_function = MiscFunctionality(bot)

    @commands.command(name="profile")
    async def bot(self):
        """
        Shows bot profile
        An example for this command would be:
        "$donate"
        """
        await self.cmd_function.display_bot_profile()

    @commands.command(name="contact")
    async def contact(self):
        """
        Shows contact information
        An example for this command would be:
        "$donate"
        """
        await self.cmd_function.display_contact()

    @commands.command(name="donate")
    async def donate(self):
        """
        Shows donation options
        An example for this command would be:
        "$donate"
        """
        await self.cmd_function.display_donation_option()


class MiscFunctionality:
    """
    Handles all Misc command functionality
    """
    def __init__(self, bot):
        self.bot = bot

    async def display_bot_profile(self):
        """
        Displays the bot profile URL
        """
        try:
            msg = "https://discordbots.org/bot/353373501274456065"
            await self.bot.say(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def display_contact(self):
        """
        Displays the owner of this bot
        """
        try:
            username = await self.bot.get_user_info(str(133108920511234048))
            msg = ("Questions? Concerns? Hit me up: **{}**".format(username))
            await self.bot.say(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def display_donation_option(self):
        """
        Displays donation message
        """
        try:
            msg = ("If you'd like to donate, you can send coins to the "
                   "following addresses:\n```"
                   "ETH: 0x13318b2A795940D119b999ECfe827708131fA3f6\n"
                   "LTC: LiChyn9o9VhppANUHDhe6ReFjGoGhLqtZm\n"
                   "```Or via paypal: https://paypal.me/Kodycode")
            await self.bot.say(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))


def setup(bot):
    bot.add_cog(MiscCommands(bot))

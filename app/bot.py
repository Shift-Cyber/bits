# python native imports
import os
import sys
import logging

# third party imports
import google.cloud.logging
import discord

from discord.ext import commands

# local imports
from cogs.registration import Registration


# inherit environment
TOKEN     = os.environ.get("DISCORD_TOKEN")
LOG_LOCAL = os.environ.get("LOG_LOCAL", 0)
VERSION   = "v1.0.2"


# logging configuration, local or remote
if int(LOG_LOCAL):
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d (%(levelname)s | %(filename)s:%(lineno)d) - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("logging set to stdout rather than GCP")
else: google.cloud.logging.Client().setup_logging()


# instantiate bot
bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')
logging.info("bits has been instantiated with intents and a command prefix")


# setup initial actions on bot ready
@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')

    # inform version in presence
    await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.watching, name=VERSION) )
    logging.info(f"bits presence set to [{VERSION}]")

    # add registration options
    await bot.add_cog(Registration(bot))
    logging.info("associated registration cog")


# start the bot with the provided access token
logging.info("starting bot")
if not bot.run(TOKEN): logging.critical("failed to start Bits or shutdown/reset")

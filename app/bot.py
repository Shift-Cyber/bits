# python native imports
import os
import sys
import logging

# third party imports
import discord
from discord.ext import commands
import google.cloud.logging

# local imports
from cogs.registration import Registration

# inherit environment
TOKEN = os.environ.get("DISCORD_TOKEN", None)
VERSION = os.environ.get("VERSION", None)

# configure logging to GCP
google.cloud.logging.Client().setup_logging()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d (%(levelname)s | %(filename)s:%(lineno)d) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# instantiate bot
bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')

# setup initial actions on bot ready
@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')

    # inform version in presence
    await bot.change_presence( activity=discord.Activity(type=discord.ActivityType.watching, name=VERSION) )

    # add registration options
    await bot.add_cog(Registration(bot))

# start the bot with the provided access token
bot.run(TOKEN)
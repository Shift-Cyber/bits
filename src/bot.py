import discord
from discord.ext import commands
from botalive import botalive
from botwhoami import botwhoami
#from botregister import botregister
from isadmin import isadmin

class Bot:
    def __init__(self, logging:object, config:object) -> None:
        self.log = logging
        self.config = config
        
        #Configure bot
            #TODO set from configuration, any intents we might need. Can also set contexts in configuration and do it that way
        intents = discord.Intents(messages=True, guilds=True, members=True) 
            #TODO set description from configuration
        description = '''A placeholder bot description.'''

        self.bot = commands.Bot(command_prefix='!', description=description, intents=intents)

        @self.bot.event
        async def on_ready():
            self.log.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')

        @self.bot.command() #TODO Break this out into a class or some other logical structure not in Bot.init
        async def alive(ctx):
           await botalive(ctx, self)
        
        @self.bot.command()
        async def adminalive(ctx):
            adminVerified = await isadmin(ctx, self)
            if adminVerified == "Yes":
                await botalive(ctx, self)
            else:
                await ctx.send("No Soup For You")

        @self.bot.command()
        async def whoami(ctx):
            await botwhoami(ctx, self)

        @self.bot.command()
        async def register(ctx):
            await botregister(ctx, self)


        #Initialize
        self.__start_bot()


    def __start_bot(self) -> None:
        token = self.config.data['bot_settings']['discord_token']
        self.bot.run(token)

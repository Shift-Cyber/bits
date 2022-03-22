import discord
import os
from discord.ext import commands

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
       
        #Logs the bot starting up
        @self.bot.event
        async def on_ready():
            self.log.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            print('Bot has been started')

        #Creates !load command that is used to load cog files. All commands are written in cog files, not in this file
        @self.bot.command()
        async def load(ctx, extension):
            self.bot.load_extension(f'cogs.{extension}')

        #Creates !unload command that is used to unload cog files.
        #Unloading and reloading adds in new commands/changes without having to restart the bot
        @self.bot.command()
        async def unload(ctx, extension):
            self.bot.unload_extension(f'cogs.{extension}')
        
        #TODO Create reload command that unloads and loads all currently loaded cog files.
        @self.bot.command()
        async def reload(ctx, extension):
            pass


        os.chdir(r"/opt/bits")

        #Gets all .py files in the ./src/cogs folder and loads them automatically on start
        #TODO Change if statement to get specific files. Not secure to get all .py files
        #for filename in os.listdir('./cogs'):
         #   if filename.endswith('.py'):
          #      self.bot.load_extension(f'cogs.{filename[:-3]}')

        #Initialize
        self.__start_bot()


    def __start_bot(self) -> None:
        token = self.config.data['bot_settings']['discord_token']
        self.bot.run(token)

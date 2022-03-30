import discord
import os
import sys
from discord.ext import commands

sys.path.insert(0, "/opt/bits/src/commands")
from alive_command import alive_command
from whoami_command import whoami_command
from admin_debug_command import admin_debug_command

class Bot:
    def __init__(self, logging:object, config:object) -> None:
        self.log = logging
        self.config = config
        adminCheck = self.config.data['bot_settings']['adminRoleId']
        
        os.chdir(r"/opt/bits/")

        #Configure bot
            #TODO set from configuration, any intents we might need. Can also set contexts in configuration and do it that way
        intents = discord.Intents(messages=True, guilds=True, members=True) 
            #TODO set description from configuration
        description = '''A placeholder bot description.'''

        self.bot = commands.Bot(command_prefix='!', description=description, intents=intents)
       
        def is_admin(ctx):
            commander = ctx.guild.get_member(ctx.author.id)
            self.log.debug(f"[{commander} role is {commander.top_role}]")
            return commander.top_role.id == adminCheck

        #Logs the bot starting up
        @self.bot.event
        async def on_ready():
            self.log.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            print('Bot has been started')
        
        #Verifies bot is online
        @self.bot.command()
        async def alive(ctx):
            await alive_command(ctx, self)
            return

        #Returns Username and Top Role
        @self.bot.command()
        async def whoami(ctx):
            await whoami_command(ctx, self)
            return

        #TODO Delete this / Used for testing commands.check
        @commands.check(is_admin) 
        @self.bot.command()
        async def admin_debug(ctx):
            await admin_debug_command(ctx, self)
            return

        #Initialize
        self.__start_bot()


    def __start_bot(self) -> None:
        token = self.config.data['bot_settings']['discord_token']
        self.bot.run(token)

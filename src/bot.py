import discord
from discord.ext import commands

class Bot:
    def __init__(self, logging:object, config:object) -> None:
        self.log = logging
        self.config = config
        
        #Configure bot
            #TODO set from configuration, any intents we might need. Can also set contexts in configuration and do it that way
        intents = discord.Intents.default() 
            #TODO set description from configuration
        description = '''A placeholder bot description.'''

        self.bot = commands.Bot(command_prefix='!', description=description, intents=intents)

        @self.bot.event
        async def on_ready():
            self.log.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')

        @self.bot.command() #TODO Break this out into a class or some other logical structure not in Bot.init
        async def alive(ctx):
            """Check daemon status from server."""
            self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
            
            
            #TODO This should be decorated as admin only

            #Send response
            message = "Still alive but I'm barely breathing... dun dun DUN DUN..."
            await ctx.send(message)
            self.log.info(f"Sever replied with '{message}'")

        #Initialize
        self.__start_bot()


    def __start_bot(self) -> None:
        token = self.config.data['bot_settings']['discord_token']
        self.bot.run(token)

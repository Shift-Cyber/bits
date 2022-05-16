import discord
import os
import sys
from discord.ext import commands

sys.path.insert(0, "/opt/bits/src/commands")
from alive_command import alive_command
from whoami_command import whoami_command
from admin_debug_command import admin_debug_command
from register_command import register_command
from whoareyou_command import whoareyou_command
from support_command import support_command
from wrench_command import wrench_command

class Bot:
    def __init__(self, logging:object, config:object) -> None:
        self.log = logging
        self.config = config
        modCheck = self.config.data['bot_settings']['modRoleID']
        adminCheck = self.config.data['bot_settings']['adminRoleId']
        compCheck = self.config.data['bot_settings']['competitorRoleID']

        os.chdir(r"/opt/bits/")

        #Configure bot
            #TODO set from configuration, any intents we might need. Can also set contexts in configuration and do it that way
        intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True) 
            #TODO set description from configuration
        description = '''A placeholder bot description.'''

        self.bot = commands.Bot(command_prefix='!', description=description, intents=intents)
       

        #Logs the bot starting up
        @self.bot.event
        async def on_ready():
            self.log.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            print('Bot has been started')
            global guild
            guild = self.bot.get_guild(self.config.data['bot_settings']['guildID'])
            print('Guild has been set to: ' + str(guild.name) + ' | ' + str(guild.id))

        ###TODO Work this event into only responding to users interacting with the !support command.
        ###Bot currently responds to all messages that reactions are added to
        @self.bot.event
        async def on_reaction_add(reaction, user):
            if user != self.bot.user:
                channel = reaction.message.channel
                if str(reaction.emoji) == '🔧':
                    await channel.send('Thats a Wrench')
                    await wrench_command(self, user, channel, guild)
                elif str(reaction.emoji) == '💡':
                    await channel.send('Thats a Bulb')
                else:
                    await channel.send('You added an unrecognized reaction')

        @self.bot.event
        async def on_reation_remove(reaction, user):
            channel = reaction.message.channel
            await self.bot.send_message(channel, '{} has removed {} from the message: {}'.format(user.name, reaction.emoji, reaction.message.content))
        
        
        #Verifies bot is online
        @commands.has_role(int(adminCheck))
        @self.bot.command()
        async def alive(ctx):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            await alive_command(ctx, self)
            return

        #Returns Username and Top Role
        @commands.has_any_role(int(modCheck), int(adminCheck))
        @self.bot.command()
        async def whoami(ctx):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            await whoami_command(ctx, guild)
            return
   
        @self.bot.command()
        async def register(ctx):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            await register_command(ctx, self)
            return 
        
        ###TODO has_any_role doesn't work with DMs. Need to find a new check
        #@commands.has_any_role(int(compCheck), int(modCheck), int(adminCheck))
        @self.bot.command()
        async def support(ctx):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            if ctx.author != self.bot.user:
                await support_command(ctx, self)
            return

        #Jokes Below This Line
        @self.bot.command(hidden=True)
        async def whoareyou(ctx):
            await whoareyou_command(ctx, self)
            return
         
        #Initialize
        self.__start_bot()


    def __start_bot(self) -> None:
        token = self.config.data['bot_settings']['discord_token']
        self.bot.run(token)

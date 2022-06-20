import discord
import os
import sys
from discord.ext import commands

sys.path.insert(0, "/opt/bits/src/commands")
from alive_command import alive_command
from whoami_command import whoami_command
from register_command import register_command
from whoareyou_command import whoareyou_command
from support_command import support_command
from userinfo_command import userinfo_command

class Bot:
    def __init__(self, logging:object, config:object) -> None:
        self.log = logging
        self.config = config
        mod_check = self.config.data['bot_settings']['modRoleID']
        admin_check = self.config.data['bot_settings']['adminRoleId']
        comp_check = self.config.data['bot_settings']['competitorRoleID']
        newb_check = self.config.data['bot_settings']['newbRoleID']
        
        #Probably not needed, written by a noob or something
        #os.chdir(r"/opt/bits/")

        #Configure bot
            #TODO set from configuration, any intents we might need. Can also set contexts in configuration and do it that way
        intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True) 
            #TODO set description from configuration
        description = '''A placeholder bot description.'''

        self.bot = commands.Bot(command_prefix='!', description=description, intents=intents)
        
        ###TODO Move filepath/name to config file. Ensure file is opened with only read permissions and is closed proper
        bw = open('/opt/bits/src/bWords.txt')
        bwlines = bw.readlines()
        b_words = []
        for i in bwlines:
            b_words.append(i[:-1])

        #Logs the bot starting up
        @self.bot.event
        async def on_ready():
            self.log.info(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
            print('Bot has been started')
            global guild
            guild = self.bot.get_guild(self.config.data['bot_settings']['guildID'])
            self.log.info(f'Guild has been set to: {guild.name} | {guild.id}')
         
        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return

            msg = message.content.lower().replace(" ","")

            if any(word in msg for word in b_words):
                vio_resp = "Hault {}, you have violated the law. you dirty slut. keep swearing and I will kill you, you little shit".format(message.author)
                await message.author.send(vio_resp)
                await message.delete()
            await self.bot.process_commands(message)
                
        #Member_check is used for commands run outside of Guild channels (ie DMs). Built-in has_role only works in Guild channels
        def member_check(ctx):
            member = guild.get_member(ctx.author.id)
            if member == "None":
                self.log.info(f'{ctx.author.name}:{ctx.author.id} exectued {ctx.invoked_with} and is NOT a member')
                return False
            else:
                newb_role = guild.get_role(newb_check)
                return member.top_role != newb_role

        
        #Verifies bot is online
        @commands.has_role(int(admin_check))
        @self.bot.command()
        async def alive(ctx):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            await alive_command(ctx, self)
            return

        #Returns Username and Top Role
        @commands.has_any_role(int(mod_check), int(admin_check))
        @self.bot.command()
        async def whoami(ctx):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            await whoami_command(ctx, guild)
            return
        
        @commands.has_any_role(int(mod_check), int(admin_check))
        @self.bot.command()
        async def userinfo(ctx, user):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            await userinfo_command(ctx, self, user, guild)
            return

        #@self.bot.command()
        #async def register(ctx):
         #   self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
         #   await register_command(ctx, self, guild)
         #   return 
        
        @self.bot.command()
        @commands.check(member_check)
        async def support(ctx):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            await support_command(ctx, self, guild)
            return

        #Jokes Below This Line
        @self.bot.command(hidden=True)
        async def whoareyou(ctx):
            self.log.info(f"{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
            await whoareyou_command(ctx, self)
            return
        
        #Initialize
        self.__start_bot()

    def __start_bot(self) -> None:
        token = self.config.data['bot_settings']['discord_token']
        self.bot.run(token)

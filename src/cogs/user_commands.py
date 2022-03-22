import discord
from discord.ext import commands

class user_commands(commands.Cog):

    def __init__(self, client):
        self.client = client    
    
    #TODO Figure out logging
    #Listener will respond when the !load command is used to load the cog file.
    @commands.Cog.listener()
    async def on_ready(self):
        #self.log.info(f'Loaded Cog user_commands')
        print('Loaded bitsCog1')
    
    #TODO Edit this to check multiple roles. Admin should be able to run moderator commands, etc
    #TODO Move role ID into config file for security
    #Creates the Check that other commands will use to limit what commands individual users can run
    def is_admin(ctx):
        #commander = ctx.guild.get_member(ctx.author.id)
        #print(f"[{commander}] [{commander.top_role}]")
        #return commander.top_role.id == #Numbers
        pass

    #TODO Add commands.check() to restrict to admin/mods
    #Creates bot command !alive that will respond to indicate it is connected and operating
    @commands.command()
    async def alive(self, ctx):
        #self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
        response = "I am Alive"
        await ctx.send(response)
        #self.log.info(f"Server replied with '{message}'")
    
    #Whoami that can returns the user's name and top role. Removed user id for security.
    @commands.command()
    async def whoami(self, ctx):
        #self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
        guild = ctx.guild
        #self.log.debug(f"Guild recorded as '{guild}'")
        you = guild.get_member(ctx.author.id)
        #self.log.debug(f"You recorded as '{you}'")
        youReturn = "You are " + str(you.name) + " and your role is " +str(you.top_role)
        await ctx.send(youReturn)
        #self.log.info(f"Server replied with '{youReturn}'")

#Loads this cog to bot.py
def setup(client):
    client.add_cog(user_commands(client))

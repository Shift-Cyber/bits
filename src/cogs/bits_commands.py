import discord
from discord.ext import commands

class bitsCog1(commands.Cog):

    def __init__(self, client):
        self.client = client    

    @commands.Cog.listener()
    async def on_ready(self):
        #self.log.info(f'Loaded bitsCog1')
        print('Loaded bitsCog1')

    @commands.command()
    async def alive(self, ctx):
        #self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
        response = "Become a Cog in the Machine"
        await ctx.send(response)
        #self.log.info(f"Server replied with '{message}'")

    #@commands.command()
    #async def whoami(self, ctx):
        #self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
        #guild = ctx.guild
        #self.log.debug(f"Guild recorded as '{guild}'")
        #you = guild.get_member(ctx.author.id)
        #self.log.debug(f"You recorded as '{you}'")
        #youReturn "You are " + str(you.name) + ", your role is " +str(you.top_role) + ", and your user id is " + str(you.id)
        #await ctx.send(youReturn)
        #self.log.info(f"Server replied with '{youReturn}'")

def setup(client):
    client.add_cog(bitsCog1(client))

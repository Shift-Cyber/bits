import discord
from discord.ext import commands

class mod_commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        #self.log.info(f'Loaded Cog mod_commands')
        print('Loaded mod_commands')

    def is_mod(ctx):
        commander = ctx.guild.get_member(ctx.author.id)
        #self.log.debug(f'is_mod check returned [{ctx.author.id}:{ctx.author}] as [{commander.id}:{commander}]')
        return commander.top_role.id == 943178954955714568

    @commands.command()
    @commands.check(is_mod)
    async def modcheck():
        success = "You Are A Moderator"
        await ctx.send(success)
        

def setup(client):
    client.add_cog(mod_commands(client))

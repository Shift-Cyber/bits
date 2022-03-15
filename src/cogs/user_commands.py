import discord
from discord.ext import commands

class user_commands(commands.Cog):

    def __init__(self, client):
        self.client = client    

    @commands.Cog.listener()
    async def on_ready(self):
        #self.log.info(f'Loaded Cog user_commands')
        print('Loaded bitsCog1')

    def is_admin(ctx):
        commander = ctx.guild.get_member(ctx.author.id)
        print(f"[{commander}] [{commander.top_role}]")
        return commander.top_role.id == 943179378072895498
        #if commander.top_role == "Administrators":
        #    return True
        #else:
        #    return False

    @commands.command()
    @commands.check(is_admin)
    async def alive(self, ctx):
        #self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
        response = "I am Alive"
        await ctx.send(response)
        #self.log.info(f"Server replied with '{message}'")

    @commands.command()
    async def whoami(self, ctx):
        #self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
        guild = ctx.guild
        #self.log.debug(f"Guild recorded as '{guild}'")
        you = guild.get_member(ctx.author.id)
        #self.log.debug(f"You recorded as '{you}'")
        youReturn = "You are " + str(you.name) + ", your role is " +str(you.top_role) + ", and your user id is " + str(you.id)
        await ctx.send(youReturn)
        #self.log.info(f"Server replied with '{youReturn}'")

def setup(client):
    client.add_cog(user_commands(client))

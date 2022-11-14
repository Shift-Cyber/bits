
from discord.ext import commands


# local imports
from structures.user import User
from connectors.database import Database


class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    """@commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')"""


    @commands.command(name="register")
    async def register(self, ctx, *args):
        if len(args) == 1:
            user = self.database.lookup_user_email(args[0])

            if user:
                await ctx.send(f'Found user {user.first_name} {user.last_name}')

        # not enough arguments
        else: await ctx.send(f'Usage: !register <email-address>')


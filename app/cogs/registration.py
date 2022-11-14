# local imports
import secrets
import time
import os

# third party imports
from discord.utils import get
from discord.ext import commands
from structures.user import User
from connectors.database import Database
from connectors.email import EmailClient

# environment setup
TOKEN_EXP_SEC = os.environ.get("TOKEN_EXP_SEC", None) or 600


class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        await ctx.send(f"""Welcome to the Hack a Bit Discord, I'm Bits, your personal assistant!""")
        time.sleep(5)
        await ctx.send(f"""Send me the register command to get started...```!register ```""")


    @commands.command(name="register")
    async def register(self, ctx, *args):
        if len(args) == 2:
            if args[0] == "get-token":
                user = self.database.lookup_user_email(args[1])

                # if the user was found
                if user:
                    # generate a 20 character pseudo-random token
                    token = secrets.token_hex(20)

                    self.database.save_token(
                        token = token,
                        email = user.email,
                        issued_epoch = int(time.time())
                    )

                    EmailClient().send_registration_code(user, token)

                await ctx.send(f'Request received, if the account exists you will receive an email with the authorization token and further instructions.')

            elif args[0] == "use-token":
                token_record = self.database.get_token_record(args[1])
                user = self.database.lookup_user_email(token_record.email)

                if token_record:
                    if not int(token_record.issued_epoch) >= (int(time.time()) + TOKEN_EXP_SEC):
                        
                        # add member role to caller
                        member = ctx.message.author
                        await member.add_roles(get(ctx.guild.roles, name="Member"), atomic=True)

                        # if registered, add competitor role to caller
                        if bool(user.registered) == True:
                            member = ctx.message.author
                            await member.add_roles(get(ctx.guild.roles, name="Competitor"), atomic=True)

                        await ctx.send(f"""Registered, {user.email} your roles have been granted!""")

                    else:
                        await ctx.send(f"""Attempted registration with an expired token, please generate a new token and try again.""")

                else: await ctx.send(f'Registration failed, invalid token.')
        
        # not the right number of arguments
        else: await ctx.send(f"""Start with this command to get a token in your email:\n```!register get-token <email-address>```Then send it back to me with this command to get assigned your roles:```!register use-token <access-token>```\n*Replace the triangle brackets '<email-address>' with yours.*""")

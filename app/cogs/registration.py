# local imports
import secrets
import time
import os
import logging

# third party imports
from discord.utils import get
from discord.ext import commands
from structures.user import User
from connectors.database import Database
from connectors.email import EmailClient

# environment setup
TOKEN_EXP_SEC = os.environ.get("TOKEN_EXP_SEC", 600)


class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        await member.send(f"""Welcome to the Hack a Bit Discord, I'm Bits, your personal assistant!""")
        time.sleep(5)
        await ctx
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
                logging.info(f"sent token [{token}] to user [{user.email}] and messaged notification to user")

            elif args[0] == "use-token":
                token_record = self.database.get_token_record(args[1])
                user = self.database.lookup_user_email(token_record.email)

                # if a token record was located in the database
                if token_record:
                    if int(token_record.issued_epoch) + int(TOKEN_EXP_SEC) >= int(time.time()):

                        # get guild and member role based on ID so the bot isnt reliant on ctx
                        guild = self.bot.get_guild(int(os.environ.get("GUILD_ID")))
                        member_role = guild.get_role(int(os.environ.get("MEMBER_ROLE")))

                        # retreive member based on id
                        member = guild.get_member(ctx.message.author.id)
                        
                        # ensure user does not have an existing registration, notify and exit if they do
                        if (user.discord_id != None) and (user.discord_id != member_id):
                            await ctx.send(f"""Your account {user.email}, was already registered with a different Discord account, please contact the @Staff to resolve!""")
                            logging.warning(f"user [{user.email}] attempted registration with a different account... was denied registration")
                        
                        # either the Discord ID in the db was None or it matched the member_id, continue on
                        else:
                            # add discord association if it doesn't exist
                            if not user.discord_id:
                                self.database.set_discord_association_uid(user.uid, member_id)
                                logging.info(f"user [{member_id}] associated with [{user.email}]")

                            # everything passes... grant roles based on prior context
                            await member.add_roles(member_role, atomic=True)
                            logging.info(f"user [{user.email}] granted member role")

                            # if registered, add competitor role to caller
                            if bool(user.registered) == True:
                                
                                # get competitor role based on ID so the bot isnt reliant on ctx
                                competitor_role = guild.get_role(int(os.environ.get("COMPETITOR_ROLE")))

                                # add role based on prior context
                                await member.add_roles(competitor_role, atomic=True)
                                logging.info(f"user [{user.email}] granted competitor role")

                            # notify user
                            await ctx.send(f"""Registered {user.email}, your roles have been granted!""")
                            logging.info(f"user [{user.email}] registered with token [{args[1]}]")

                    else:
                        await ctx.send(f"""Attempted registration with an expired token, please generate a new token and try again.""")
                        logging.info(f"user [{user.email}] attempted registration with expired token [{args[0]}]")

                else: await ctx.send(f'Registration failed, invalid token.')
        
        # not the right number of arguments
        else: await ctx.send(f"""Start with this command to get a token in your email:\n```!register get-token <email-address>```Then send it back to me with this command to get assigned your roles:```!register use-token <access-token>```\n*Replace the triangle brackets '<email-address>' with yours.*""")

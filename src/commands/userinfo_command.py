import discord

###TODO Command struggles with special characters, figure it out
async def userinfo_command(ctx, self, user, guild):
    member:str = discord.utils.find(lambda m: m.name == user, guild.members)
    roles = []
    for role in member.roles:
        roles.append(role.name)
    member_info = f'Username:{member.name} | Nickname:{member.nick} | Roles:{roles}'
    await ctx.send(member_info)

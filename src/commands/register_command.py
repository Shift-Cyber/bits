import discord

async def register_command(ctx, self):
    guild = ctx.guild
    userInvoked = guild.get_member(ctx.author.id)
    channelInvoked = ctx.channel

    def convCheck(m):
        return m.author == userInvoked and m.channel == channelInvoked

    await ctx.send("What is your First Name?")

    msg = await self.bot.wait_for("message", check=convCheck)
    firstName = str(msg.content)
    
    await ctx.send("What is your Last Name?")
    lastName = str(msg.content)

    fullName = firstName + " " + lastName
    await userInvoked.edit(nick=fullName)
    
    competitorRole = guild.get_role(self.config.data['bot_settings']['competitorRoleID'])

    await userInvoked.add_roles(competitorRole,
            reason=f'{ctx.author} registered for Hack-A-Bit'
            )

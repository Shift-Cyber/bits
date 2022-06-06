async def register_command(ctx, self, guild):
    user_invoked = guild.get_member(ctx.author.id)
    
    user_chat = await user_invoked.send("Starting User Registration with Hack-A-Bit:\nWhat is your First Name?")
    
    def conv_check(m):
        return m.author == user_invoked and m.channel == user_chat.channel

    msg = await self.bot.wait_for("message", check=conv_check)
    first_name = str(msg.content)
    
    await user_chat.channel.send("What is your Last Name?")
    last_name = str(msg.content)

    full_name = first_name + " " + last_name
    await user_invoked.edit(nick=full_name)
    
    competitor_role = guild.get_role(self.config.data['bot_settings']['competitorRoleID'])

    await user_invoked.add_roles(competitor_role,
            reason=f'{userInvoked} registered for Hack-A-Bit'
            )

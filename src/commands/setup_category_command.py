async def setup_category(ctx, self):
    guild = ctx.guild
    userInvoked = guild.get_member(ctx.author.id)
    channelInvoked = ctx.channel

    def convCheck(m):
        return m.author == userInvoked and m.channel == channelInvoked

    await ctx.send("What is your team's name?")

    msg = await bot.wait_for("message", check=convCheck)
    teamName = str(msg.content)

    await guild.create_role(
            name=teamName, 
            permissions=discord.Permissions(self.config.data['bot_settings']['teamRolePermissions']),
            hoist=True,
            mentionable=False,
            reason=f'{ctx.author} requested registration of {teamName}'
            )
    
    await userInvoked.add_roles(discord.utils.get(guild.roles,name=teamName),
            reason=f'{ctx.author} assigned to new team: {teamName}'
            )


    overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),


    await guild.create_category(
            name=teamName,
            overwrites=self.config.data['bot_settings']['teamCatPermissions'] ,
            topic=f'{teamName}',
            reason=f'Category created by request of {ctx.author} for {teamName}',

    





    guild.create_category()

    guild.create_category_channel()

    guild.create_text_channel()

    guild.create_voice_channel()

    guild.create_role()



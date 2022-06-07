async def whoami_command(ctx, self):
    self.log.info(f"[{ctx.author.id}:{ctx.author} executed command '{ctx.invoked_with}'")
    guild = ctx.guild
    self.log.debug(f"Guild recorded as '{guild}'")
    you = guild.get_member(ctx.author.id)
    self.log.debug(f"You recorded as '{you}'")
    you_return = "You are " +str(you.name) + " and your role is " + str(you.top_role)
    await ctx.send(youReturn)
    self.log.info(f"Server replied with '{you_return}'")

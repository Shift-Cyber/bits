async def botwhoami(ctx, self):
    self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
    guild = ctx.guild
    self.log.debug(f"Guild recorded as '{guild}'")
    you = guild.get_member(ctx.author.id)
    self.log.debug(f"You recorded as '{you}")
    youReturn = "You are " + str(you.name) + ", your role is " +str(you.top_role) + ", and your user id is " + str(you.id)
    await ctx.send(youReturn)
    self.log.info(f"Server replied with '{youReturn}'")

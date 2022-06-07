async def alive_command(ctx, self):
    self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
    response = "I am Alive"
    await ctx.send(response)
    self.log.debug(f"Server replied with '{response}'")
    return

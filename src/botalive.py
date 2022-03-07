async def botalive(ctx, self):
    #Check daemon status from server#
    self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
    #Send Response
    message = "Stop poking me"
    await ctx.send(message)
    self.log.info(f"Server replied with '{message}'")

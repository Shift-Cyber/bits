async def isadmin(ctx, self):
    self.log.info(f"[{ctx.author.id}:{ctx.author}] executed command '{ctx.invoked_with}'")
    guild = ctx.guild
    self.log.debug(f"Guild recorded as '{guild}'")
    you = guild.get_member(ctx.author.id)
    self.log.debug(f"You recorded as '{you}'")
    if you.top_role == "Administrators":
        adminRole = "Yes"
    else:
        adminRole = "No"
    self.log.debug(f"'{you}' has '{you.roles}' roles")
    return adminRole


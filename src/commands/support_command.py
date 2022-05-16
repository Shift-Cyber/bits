import discord

async def support_command(ctx, self):
    user = ctx.author

    helpMessage = f'@{user.name}, How can I help you? React to this message to receive assistance:\n🔧: Wrench Stuff\n💡: Bulb Stuff'
    
    # U0001F527 = Wrench | U0001F4A1 = Bulb
    emojis = ['\U0001F527','\U0001F4A1']
    
    helpChat = await user.send(content=helpMessage)
    for emoji in emojis:
        await helpChat.add_reaction(emoji)

import discord
from wrench_command import wrench_command

async def support_command(ctx, self, guild):
    customer = ctx.author

    helpMessage = f'@{customer.name}, How can I help you? React to this message to receive assistance:\n🔧: Wrench Stuff\n💡: Bulb Stuff'
    
    # U0001F527 = Wrench | U0001F4A1 = Bulb
    emojis = ['\U0001F527','\U0001F4A1']
    
    helpChat = await customer.send(content=helpMessage)
    for emoji in emojis:
        await helpChat.add_reaction(emoji)
    
    helpChannel = helpChat.channel
    
    def reactionCheck(reaction, user):
        return user == customer and reaction.message.channel == helpChannel
    
    ###TODO Add a timeout
    async def reactionReply():
        reaction, user = await self.bot.wait_for('reaction_add', check=reactionCheck)
        
        if reaction.emoji == emojis[0]: #Wrench
            await wrench_command(self, user, helpChannel, guild)
        elif reaction.emoji == emojis[1]: #Bulb
            await helpChannel.send('Thats a Bulb')
        
        else:
            await helpChannel.send('Unrecognized Reaction. Please try again')
        await reactionReply()
        
    await reactionReply()

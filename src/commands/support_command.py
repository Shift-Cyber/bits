from ticket_command import ticket_command

async def support_command(ctx, self, guild):
    customer = ctx.author
    
    wrench_text:str = 'Something isn\'t working right or you think something is broken'
    bulb_text:str = 'You can\'t log in to an account or you have a permissions error'

    help_message = f'@{customer.name}, How can I help you? React to this message to receive assistance:\n🔧: {wrench_text}\n💡: {bulb_text}'
    
    emojis = {'wrench':'\U0001F527','bulb':'\U0001F4A1']

    help_chat = await customer.send(content=help_message)
    for emoji in emojis:
        await help_chat.add_reaction(emoji)
    
    broken_channel = guild.get_channel(self.config.data['bot_settings']['brokenChannelID'])
    account_channel = guild.get_channel(self.config.data['bot_settings']['accountChannelID'])

    def reaction_check(reaction, user):
        return user == customer and reaction.message.channel == help_chat.channel
    
    ###TODO Add a timeout | Create Ticket numbering system
    async def reaction_reply():
        reaction, user = await self.bot.wait_for('reaction_add', check=reaction_check)
        if reaction.emoji == emojis['wrench']: 
            ticket_channel = broken_channel
            await ticket_command(self, user, help_chat.channel, guild, ticket_channel)
        elif reaction.emoji == emojis['bulb']: 
            ticket_channel = account_channel
            await ticket_command(self, user, help_chat.channel, guild, ticket_channel)
        else:
            await help_chat.channel.send('Unrecognized Reaction. Please try again')
        await reaction_reply()
        
    await reaction_reply()

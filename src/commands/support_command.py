from ticket_command import ticket_command

async def support_command(ctx, self, guild):
    customer = ctx.author

    help_message = f'@{customer.name}, How can I help you? React to this message to receive assistance:\n🔧: Wrench Stuff\n💡: Bulb Stuff'
    
    # U0001F527 = Wrench | U0001F4A1 = Bulb
    emojis = ['\U0001F527','\U0001F4A1']

    help_chat = await customer.send(content=help_message)
    for emoji in emojis:
        await help_chat.add_reaction(emoji)
    
    wrench_channel = guild.get_channel(self.config.data['bot_settings']['wrenchChannelID'])
    bulb_channel = guild.get_channel(self.config.data['bot_settings']['bulbChannelID'])

    def reaction_check(reaction, user):
        return user == customer and reaction.message.channel == help_chat.channel
    
    ###TODO Add a timeout | Create Ticket numbering system
    async def reaction_reply():
        reaction, user = await self.bot.wait_for('reaction_add', check=reaction_check)
        if reaction.emoji == emojis[0]: #Wrench
            ticket_channel = wrench_channel
            await ticket_command(self, user, help_chat.channel, guild, ticket_channel)
        elif reaction.emoji == emojis[1]: #Bulb
            ticket_channel = bulb_channel
            await ticket_command(self, user, help_chat.channel, guild, ticket_channel)
        else:
            await help_chat.channel.send('Unrecognized Reaction. Please try again')
        await reaction_reply()
        
    await reaction_reply()

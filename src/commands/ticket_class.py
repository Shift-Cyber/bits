class Ticket:
    def __init__(self, number, customer, ticket_channel, description):
        self.number = number
        self.customer = customer
        self.ticket_channel = ticket_channel
        self.description = description
        self.emojis = {'red_square':'\U0001F7E5','yellow_square':'\U0001F7E8','green_square':'\U0001F7E9'}
    
    async def create_ticket(self):
        ticket_message = f"{self.number} | {self.customer.name} | {self.description.content}"
        self.ticket_thread = await self.ticket_channel.send(str(ticket_message))
        await self.ticket_thread.create_thread(name=self.number)

        #1F7E5 = Red Square | 1F7E8 = Yellow Square | 1F7E9 = Green Square
        for emoji in self.emojis.values():
            await self.ticket_thread.add_reaction(emoji)

    async def message_user(self):
        await self.customer.send('The moderator has sent you this message')
        return

    async def message_mod(self):
        await self.ticket_channel.send('The user has sent you this message')
        return

    async def reaction_reply(self, reaction):
        #reaction, user = await self.bot.wait_for('reaction_add',check=reaction_check)
        if reaction.emoji == self.emojis['red_square']:
            await self.message_user()
        elif reaction.emoji == self.emojis['yellow_square']:
            await self.message_mod()
        elif reaction.emoji == self.emojis['green_square']:
            pass
        else:
            pass

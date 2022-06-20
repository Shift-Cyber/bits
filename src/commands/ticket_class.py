class Ticket:
    def __init__(self, number, customer, ticket_channel, description):
        self.number = number
        self.customer = customer
        self.ticket_channel = ticket_channel
        self.description = description

    async def create_ticket(self):
        ticket_message = f"{self.number} | {self.customer.name} | {self.description.content}"
        self.ticket_thread = await self.ticket_channel.send(str(ticket_message))

        #1F7E5 = Red Square | 1F7E8 = Yellow Square | 1F7E9 = Green Square
        emojis = ['red_square':'\U0001F7E5','yellow_square':'\U0001F7E8','green_square':'\U0001F7E9']
        for emoji in emojis:
            await self.ticket_thread.add_reaction(emoji)

    ###TODO Methods don't seem to work with this Class and the Bot
    async def message_user(self):
        print('Called message_user')
        await self.customer.send('The moderator has sent you this message')

    async def message_mod(self):
        await self.ticket_channel.send('The user has sent you this message')

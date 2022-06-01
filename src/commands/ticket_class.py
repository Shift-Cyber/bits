import discord

class Ticket:
    def __init__(self, number, customer, supportChannel, description):
        self.number = number
        self.customer = customer
        self.supportChannel = supportChannel
        self.description = description

    async def create_ticket(self):
        supportMessage = f"{self.number} | {self.customer.name} | {self.description.content}"
        self.supportThread = await self.supportChannel.send(str(supportMessage))

        #1F7E5 = Red Square | 1F7E8 = Yellow Square | 1F7E9 = Green Square
        emojis = ['\U0001F7E5','\U0001F7E8','\U0001F7E9']
        for emoji in emojis:
            await self.supportThread.add_reaction(emoji)

    async def message_user(self):
        print('Called message_user')
        await self.customer.send('The moderator has sent you this message')

    async def message_mod(self):
        await self.supportChannel.send('The user has sent you this message')

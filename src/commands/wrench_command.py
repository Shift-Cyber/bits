from ticket_class import Ticket

async def wrench_command(self, customer, channel, guild):
    wrenchMessage = f'Please describe the problem in one message and a moderator will be contacted'
    wrenchChannel = guild.get_channel(self.config.data['bot_settings']['wrenchChannelID'])
    
    def convCheck(m):
        return m.author == customer and m.channel == channel

    await channel.send(str(wrenchMessage))

    description = await self.bot.wait_for("message", check=convCheck)
      
    customerTicket = Ticket(111, customer, wrenchChannel, description)
    await customerTicket.create_ticket()

    await channel.send(str(f'Ticket #{customerTicket.number} has been sent to the moderators'))

    def reactionCheck(reaction, user):
        return reaction.message.reference == customerTicket.supportThread
       
        
    async def reactionReply():
        reaction, user = await self.bot.wait_for('reaction_add')#check=reactionCheck)
        
        if reaction.emoji == '\U0001F7E5': #Red Square
            await customer.send(str('The moderator has sent you this message'))
        elif reaction.emoji == '\U0001F7E8': #Yellow Square
            customerTicket.message_mod
            print(str('Yellow Square'))
        else:
            pass
        await reactionReply()

    await reactionReply()
        


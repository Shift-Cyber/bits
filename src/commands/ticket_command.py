from ticket_class import Ticket

async def ticket_command(self, customer, channel, guild, ticket_channel):
    ticket_message = f'Please describe the problem in one message and a moderator will be contacted'
    
    emojis = {'red_square':'\U0001F7E5','yellow_square':'\U0001F7E8','green_square':'\U0001F7E9'}

    def conv_check(m):
        return m.author == customer and m.channel == channel

    await channel.send(str(ticket_message))

    description = await self.bot.wait_for("message", check=conv_check)
    
    ###TODO Create unique ticket numbers system
    customer_ticket = Ticket(111, customer, ticket_channel, description)
    await customer_ticket.create_ticket()

    await channel.send(str(f'Ticket #{customer_ticket.number} has been sent to the moderators'))
    
    def reaction_check(reaction, user):
        return reaction.message == customer_ticket.ticket_thread
        
    emojis = {'red_square':'\U0001F7E5','yellow_square':'\U0001F7E8','green_square':'\U0001F7E9'}

    async def reaction_reply():
        reaction, user = await self.bot.wait_for('reaction_add',check=reaction_check)    
        if reaction.emoji == emojis['red_square']:
<<<<<<< HEAD
            #await customer.send(str('The moderator has sent you this message'))
            customer_ticket.message_user()
            print (str('Red Square'))
        elif reaction.emoji == emojis['yellow_square']:
            customer_ticket.message_mod()
            print(str('Yellow Square'))
        elif reaction.emoji == emojis['green_square']:
            print(str('Green Square'))
=======
            await customer.send(str('The moderator has sent you this message'))
            print ('Red Square')
        elif reaction.emoji == emojis['yellow_square']:
            customer_ticket.message_mod()
            print('Yellow Square')
        elif reaction.emoji == emojis['green_square']:
            print('Green Square')
>>>>>>> 2c475432fa6b03f2d4ad8d885afa34a3adf99522
        else:
            pass
        await reaction_reply()

    await reaction_reply()
        


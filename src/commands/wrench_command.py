async def wrench_command(self, user, channel, guild):
    wrenchMessage = f'Please describe the problem in one message and a moderator will be contacted'
    wrenchChannel = guild.get_channel(self.config.data['bot_settings']['wrenchChannelID'])
    
    def convCheck(m):
        return m.author == user and m.channel == channel

    await channel.send(str(wrenchMessage))

    problemDescription = await self.bot.wait_for("message", check=convCheck)
   
    channelMessage = f"{user.name} has reported a potential bug with the following description:\n{problemDescription.content}"

    await wrenchChannel.send(str(channelMessage))

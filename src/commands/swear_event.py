from comp_class import Comp

async def swear_event(self, message):
    await message.delete()

    filthy_swearer = Comp(message.author)
    await filthy_swearer.swear()
    did_swear = True
        
    if did_swear == True and filthy_swearer.swear_jar == 1:
        swear_response = "You have been detected swearing and your message has been deleted. Please review Hack-A-Bit community guidelines."
    #elif did_swear == True and filthy_swearer.swear_jar > 1: 
        #swear_response = f"You have sworn {filthy_swearer.swear_jar} times. Continued violations of community guidelines may result in moderator actions such as timeouts and muting."
    else:
        return

    await message.author.send(swear_response)
    return
    

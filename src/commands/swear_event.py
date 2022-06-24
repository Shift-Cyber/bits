from comp_class import Comp

async def swear_event(self, ctx, message):
    msg = message.content.lower().replace(" ","")

    swear_response = "stahp swear :("
    
    if any(word in msg for word in b_words):
        await message.delete()

        filthy_swearer = Comp(message.author)
        filthy_swearer.swear()

    if filthy_swearer.swear_jar == 1:
        swear_response = "This is your first swearing violation, please review Hack-A-Bit Community Guidelines"

    elif filthy_swearer.swear_jar > 1 and filthy_swearer.swear_jar < 4:
        swear_response = f"You have sworn {filthy_swearer.swear_jar} times. If you continue, you will receive increasing chat timeouts."
    elif filthy_swearer.swear_jar > 5:
        swear_response = f"You have sworn {filthy_swearer.swear_jar} times. You will now incur increasing chat timeouts for further violations. You may contact a moderator if you feel this is in error"
        


    await message.author.send(swear_response)
    return
    

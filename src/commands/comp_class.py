#Comp as in competitor
###TODO Add in swear loggin?
class Comp:
    def __init__(self, discord_user):
        self.discord_user = discord_user
        self.swear_jar = 0
        #self.swear_list = []
    
    async def swear(self):
        #self.swear_list.append(swear_message)
        self.swear_jar += 1

    async def reset_swear(self):
        #self.swear_list.clear()
        self.swear_count = 0

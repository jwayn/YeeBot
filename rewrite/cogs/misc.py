from discord.ext import commands

class Misc:
    def __init__(self, yeebot):
        self.yeebot = yeebot

    @commands.command()
    async def info(self):
        yeestring = ('**YeeBot is currently in alpha.**\n'
                     'He is being worked on by yust.\n'
                     'Progress can be tracked at: '
                     '<https://trello.com/b/70M7ljxB/yeebot>\n'
                     'You can help out with building him at: '
                     '<https://github.com/jaspric/YeeBot/>')
        return await self.yeebot.say(yeestring)

def setup(yeebot):
    yeebot.add_cog(Misc(yeebot))

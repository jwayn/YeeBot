import random
import discord
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
    
    @commands.command(hidden=True)
    async def sputnik(self):
        return await self.yeebot.say('http://imgur.com/HPdBflu')

    
    @commands.command(pass_context=True)
    async def roll(self, ctx, rstring):
        name = ctx.message.author.name
        roll  = rstring.lower().split('d')
        mod = roll[0]
        die = roll[1]
        results = []
        elstring = 'Please use the format `!roll <[1]-10>d<4|6|8|10|12|20|100>`.'
        if mod:
            try:
                if int(mod) <= 10 and int(mod) > 0:
                    if die in ['4', '6', '8', '10', '12', '20', '100']:
                        for x in range(0, int(mod)):
                            this_roll = random.randrange(1, int(die) + 1)
                            results.append(this_roll)
                        rstring = ', '.join(str(x) for x in results)
                        return await self.yeebot.say("{} rolled a d{} {} times and got `{}`!"
                                                .format(name, die, mod, rstring))
                    else:
                        return await self.yeebot.say(elstring)
                else:
                    return await self.yeebot.say(elstring)
            except ValueError:
                return await self.yeebot.say(elstring + 'valueerror')
        else:
            if die in ['4', '6', '8', '10', '12', '20', '100']:
               this_roll = random.randrange(1, int(die) + 1)
               return await self.yeebot.say("{} rolled a d{} and got `{}`!".format(name, die, str(this_roll)))
            else:
                return await self.yeebot.say(elstring)

def setup(yeebot):
    yeebot.add_cog(Misc(yeebot))
